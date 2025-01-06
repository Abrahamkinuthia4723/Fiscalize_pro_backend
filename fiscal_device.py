from flask import Flask, request, jsonify
import random
import qrcode
import os

app = Flask(__name__)

# Configuration for storing QR codes
app.config['UPLOAD_FOLDER'] = 'static/qr_codes'

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

    # Simulate a signature for the fiscalized invoice
    signature = f"Signature-{random.randint(1000, 9999)}"

    # Return the simulated fiscalization response
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

if __name__ == '__main__':
    app.run(port=5001, debug=True)
