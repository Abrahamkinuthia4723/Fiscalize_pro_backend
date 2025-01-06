from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import requests
from datetime import datetime
from flask_cors import CORS
import random
import qrcode
import os
from models import DBoInvnum, Invlines, FiscalData, db  

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fiscal_invoices.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = 'static/qr_codes'

    db.init_app(app)
    Migrate(app, db)
    CORS(app)

    @app.route('/fiscalize', methods=['POST'])
    def fiscalize_invoice():
        """Simulate fiscalizing an invoice."""
        data = request.json

        if not data or 'invoice_id' not in data or 'items' not in data:
            return jsonify({'status': 'error', 'message': 'Invalid request data!'}), 400

        invoice_id = data['invoice_id']
        items = data['items']

        # Generate a QR code for the invoice
        qr_code_path = generate_qr_code(invoice_id, items)
        signature = f"Signature-{random.randint(1000, 9999)}"

        response = {
            'status': 'success',
            'qr_code_path': qr_code_path,
            'signature': signature
        }

        return jsonify(response)

    def generate_qr_code(invoice_id, items):
        """Generate a QR code for the fiscalized invoice."""
        qr_code_filename = f'fiscalized_invoice_{invoice_id}.png'
        qr_code_path = os.path.join(app.config['UPLOAD_FOLDER'], qr_code_filename)

        # Create QR code content
        qr_content = f"Invoice ID: {invoice_id}, Items: {items}"

        # Generate and save the QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_content)
        qr.make(fit=True)
        img = qr.make_image(fill="black", back_color="white")

        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        img.save(qr_code_path)

        return qr_code_path

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
            response = requests.post(f"http://127.0.0.1:5000/fiscalize", json=payload)
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

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)

