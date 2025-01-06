from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import requests
from datetime import datetime
from flask_cors import CORS
from models import DBoInvnum, Invlines, FiscalData, db

# Initialize extensions
migrate = Migrate()
cors = CORS()

# Fiscal device API URL
FISCAL_DEVICE_API_URL = 'http://127.0.0.1:5001/fiscalize'

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)

    # Database and configuration settings
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fiscal_invoices.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)

    @app.route('/invoices', methods=['GET'])
    def get_today_invoices():
        """Fetch all invoices created today."""
        invoices = get_invoices_created_today()
        if not invoices:
            return jsonify({'message': 'No invoices found for today.'}), 404
        return jsonify(format_invoices_response(invoices))

    @app.route('/process_invoices', methods=['POST'])
    def process_invoices():
        """Fiscalize selected invoices."""
        selected_invoices = request.json.get('selected_invoices')
        if not selected_invoices:
            return jsonify({'error': 'No invoices selected!'}), 400

        for invoice_id in selected_invoices:
            invoice = get_invoice_by_id(invoice_id)
            if not invoice:
                return jsonify({'error': f'Invoice ID {invoice_id} not found!'}), 404
            try:
                process_invoice(invoice)
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        return jsonify({'message': 'Invoices fiscalized successfully!'})

    return app

def get_invoices_created_today():
    """Get all invoices created today."""
    today = datetime.now().date()
    return DBoInvnum.query.filter(db.func.date(DBoInvnum.created_at) == today).all()

def format_invoices_response(invoices):
    """Format invoice data for API response."""
    return [
        {
            'id': invoice.id,
            'invoice_number': invoice.invoice_number,
            'customer_name': invoice.customer_name,
            'total_amount': str(invoice.total_amount),
            'created_at': invoice.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
        for invoice in invoices
    ]

def get_invoice_by_id(invoice_id):
    """Fetch an invoice by its ID."""
    return DBoInvnum.query.get(invoice_id)

def process_invoice(invoice):
    """Send the invoice to the fiscal device for processing."""
    items = get_invoice_items(invoice.id)
    item_objects = format_items_for_fiscalization(items)

    payload = {
        'invoice_id': invoice.id,
        'items': item_objects
    }

    try:
        # Send the invoice data to the fiscal device API
        response = requests.post(FISCAL_DEVICE_API_URL, json=payload)
        response_data = response.json()

        if response.status_code == 200 and response_data['status'] == 'success':
            qr_code_path = response_data['qr_code_path']
            signature = response_data['signature']
            save_fiscal_data(invoice.id, qr_code_path, signature)
        else:
            raise Exception(f"Fiscal device error: {response_data.get('message', 'Unknown error')}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to connect to the fiscal device API: {e}")

def get_invoice_items(invoice_id):
    """Fetch invoice items by invoice ID."""
    return Invlines.query.filter_by(invid=invoice_id).all()

def format_items_for_fiscalization(items):
    """Format invoice items for fiscalization."""
    return [
        {
            'item_name': item.item_name,
            'item_code': item.item_code,
            'description': item.description,
            'quantity': item.quantity,
            'price': str(item.price),
            'total_price': str(item.quantity * item.price),
            'tax_rate': str(item.tax_rate),
            'discount': str(item.discount),
        }
        for item in items
    ]

def save_fiscal_data(invoice_id, qr_code_path, signature):
    """Save fiscal data for an invoice."""
    fiscal_data = FiscalData(invid=invoice_id, qr_code_path=qr_code_path, signature=signature)
    db.session.add(fiscal_data)
    db.session.commit()

if __name__ == '__main__':
    app = create_app()
    