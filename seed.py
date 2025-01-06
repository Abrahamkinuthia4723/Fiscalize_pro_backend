from app import create_app, db  # Import the create_app function and db object
from models import DBoInvnum, Invlines, FiscalData  # Make sure you import the correct models
from datetime import date, datetime
import random

def seed_data():
    db.drop_all()
    db.create_all()

    # Sample data for invoices 
    invoices_data = [
        {'invoice_number': 'INV001', 'customer_name': 'Apple Inc.', 'total_amount': 2000.0, 'created_at': datetime.now()},
        {'invoice_number': 'INV002', 'customer_name': 'Tesla Motors', 'total_amount': 15000.0, 'created_at': datetime.now()},
        {'invoice_number': 'INV003', 'customer_name': 'Microsoft Corp.', 'total_amount': 1200.0, 'created_at': datetime.now()},
        {'invoice_number': 'INV004', 'customer_name': 'Amazon', 'total_amount': 5000.0, 'created_at': datetime.now()},
        {'invoice_number': 'INV005', 'customer_name': 'Nike', 'total_amount': 3500.0, 'created_at': datetime.now()},
        {'invoice_number': 'INV006', 'customer_name': 'Google', 'total_amount': 2200.0, 'created_at': datetime.now()},
        {'invoice_number': 'INV007', 'customer_name': 'Coca-Cola', 'total_amount': 1900.0, 'created_at': datetime.now()},
        {'invoice_number': 'INV008', 'customer_name': 'PepsiCo', 'total_amount': 1800.0, 'created_at': datetime.now()},
        {'invoice_number': 'INV009', 'customer_name': 'Facebook', 'total_amount': 8000.0, 'created_at': datetime.now()},
        {'invoice_number': 'INV010', 'customer_name': 'Samsung Electronics', 'total_amount': 6000.0, 'created_at': datetime.now()}
    ]

    # Create and add invoices
    invoices = []
    for data in invoices_data:
        invoice = DBoInvnum(
            invoice_number=data['invoice_number'],
            customer_name=data['customer_name'],
            total_amount=data['total_amount'],
            created_at=data['created_at']
        )
        invoices.append(invoice)

    db.session.add_all(invoices)
    db.session.commit()

    # Sample data for invoice lines (items) 
    invoice_lines_data = [
        {'inv_id': 1, 'item_name': 'iPhone 15 Pro', 'item_code': 'IP15P', 'description': 'Latest model of the iPhone with A17 chip and ProMotion display', 'quantity': 2, 'price': 1000.0, 'tax_rate': 10.0, 'discount': 5.0},
        {'inv_id': 1, 'item_name': 'MacBook Pro 16"', 'item_code': 'MBP16', 'description': 'High-performance laptop with Apple M2 Pro chip and 32GB RAM', 'quantity': 1, 'price': 1500.0, 'tax_rate': 10.0, 'discount': 5.0},
        {'inv_id': 2, 'item_name': 'Tesla Model S', 'item_code': 'TSMS', 'description': 'Electric car with autopilot and 370 miles range', 'quantity': 1, 'price': 35000.0, 'tax_rate': 10.0, 'discount': 7.0},
        {'inv_id': 2, 'item_name': 'Tesla Powerwall', 'item_code': 'TSWP', 'description': 'Home battery backup with solar panel integration', 'quantity': 2, 'price': 5000.0, 'tax_rate': 10.0, 'discount': 5.0},
        {'inv_id': 3, 'item_name': 'Surface Pro 9', 'item_code': 'SP9', 'description': 'Laptop-tablet hybrid with Intel Core i7 and 16GB RAM', 'quantity': 3, 'price': 1000.0, 'tax_rate': 10.0, 'discount': 5.0},
        {'inv_id': 3, 'item_name': 'Xbox Series X', 'item_code': 'XBX', 'description': 'Next-gen gaming console with 4K gaming and 1TB storage', 'quantity': 1, 'price': 500.0, 'tax_rate': 10.0, 'discount': 5.0},
        {'inv_id': 4, 'item_name': 'Amazon Echo Show 10', 'item_code': 'AE10', 'description': 'Smart display with Alexa and a 10" screen', 'quantity': 5, 'price': 150.0, 'tax_rate': 10.0, 'discount': 5.0},
        {'inv_id': 4, 'item_name': 'Ring Video Doorbell Pro 2', 'item_code': 'RVDB', 'description': 'Smart doorbell with HD video and two-way audio', 'quantity': 3, 'price': 250.0, 'tax_rate': 10.0, 'discount': 5.0},
        {'inv_id': 5, 'item_name': 'Nike Air Max 270', 'item_code': 'NAM270', 'description': 'Men\'s sports shoes with Air cushioning and lightweight design', 'quantity': 3, 'price': 150.0, 'tax_rate': 10.0, 'discount': 10.0},
        {'inv_id': 5, 'item_name': 'Nike Training Shorts', 'item_code': 'NTSh', 'description': 'Comfortable shorts for training and exercise', 'quantity': 2, 'price': 50.0, 'tax_rate': 10.0, 'discount': 5.0},
        {'inv_id': 6, 'item_name': 'Google Pixel 8', 'item_code': 'GP8', 'description': 'Smartphone with Tensor G3 chip and 48MP camera', 'quantity': 1, 'price': 900.0, 'tax_rate': 10.0, 'discount': 5.0},
        {'inv_id': 7, 'item_name': 'Coca-Cola 500ml', 'item_code': 'CC500', 'description': 'Classic Coca-Cola soda in a 500ml bottle', 'quantity': 10, 'price': 1.5, 'tax_rate': 10.0, 'discount': 0.0},
        {'inv_id': 7, 'item_name': 'Coca-Cola 1L', 'item_code': 'CC1L', 'description': 'Larger bottle of Coca-Cola soda in 1 liter size', 'quantity': 5, 'price': 3.0, 'tax_rate': 10.0, 'discount': 0.0},
        {'inv_id': 8, 'item_name': 'Pepsi 500ml', 'item_code': 'P500', 'description': 'Classic Pepsi soda in a 500ml bottle', 'quantity': 10, 'price': 1.5, 'tax_rate': 10.0, 'discount': 0.0},
        {'inv_id': 8, 'item_name': 'Pepsi 1L', 'item_code': 'P1L', 'description': 'Larger bottle of Pepsi soda in 1 liter size', 'quantity': 5, 'price': 3.0, 'tax_rate': 10.0, 'discount': 0.0},
        {'inv_id': 9, 'item_name': 'Oculus Quest 2', 'item_code': 'OQ2', 'description': 'Virtual reality headset with 128GB storage', 'quantity': 2, 'price': 300.0, 'tax_rate': 10.0, 'discount': 5.0},
        {'inv_id': 9, 'item_name': 'Meta Quest Pro', 'item_code': 'MQP', 'description': 'Advanced virtual reality headset with improved display and sensors', 'quantity': 1, 'price': 800.0, 'tax_rate': 10.0, 'discount': 5.0},
        {'inv_id': 10, 'item_name': 'Samsung Galaxy S23', 'item_code': 'SGS23', 'description': 'Flagship smartphone with Snapdragon 8 Gen 2 and 12GB RAM', 'quantity': 1, 'price': 1200.0, 'tax_rate': 10.0, 'discount': 5.0},
        {'inv_id': 10, 'item_name': 'Samsung Galaxy Buds 2', 'item_code': 'SGB2', 'description': 'Wireless earbuds with active noise cancellation', 'quantity': 2, 'price': 150.0, 'tax_rate': 10.0, 'discount': 5.0}
    ]

    # Create and add invoice lines (items)
    invoice_lines = []
    for data in invoice_lines_data:
        line = Invlines(
            invid=data['inv_id'],  
            item_name=data['item_name'],
            item_code=data['item_code'],
            description=data['description'],
            quantity=data['quantity'],
            price=data['price'],
            tax_rate=data['tax_rate'],
            discount=data['discount']
        )
        invoice_lines.append(line)

    db.session.add_all(invoice_lines)
    db.session.commit()

    print("Database seeded successfully!")

if __name__ == '__main__':
    app = create_app()  
    with app.app_context():  
        seed_data()