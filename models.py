from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Model for dbo_invnum table
class DBoInvnum(db.Model):
    __tablename__ = 'dbo_invnum'

    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(100), nullable=False)
    customer_name = db.Column(db.String(255), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    # Relationship with Invlines
    invlines = db.relationship('Invlines', backref='invoice', lazy=True)


# Model for invlines table
class Invlines(db.Model):
    __tablename__ = 'invlines'

    id = db.Column(db.Integer, primary_key=True)
    invid = db.Column(db.Integer, db.ForeignKey('dbo_invnum.id'), nullable=False)
    item_name = db.Column(db.String(255), nullable=False)
    item_code = db.Column(db.String(100), nullable=True)
    description = db.Column(db.String(255), nullable=True)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    tax_rate = db.Column(db.Float, nullable=True)
    discount = db.Column(db.Float, nullable=True)

    # Relationship with FiscalData using back_populates
    fiscal_data = db.relationship('FiscalData', back_populates='invline', lazy=True)


# Model for fiscal_data table
class FiscalData(db.Model):
    __tablename__ = 'fiscal_data'

    id = db.Column(db.Integer, primary_key=True)
    invid = db.Column(db.Integer, db.ForeignKey('invlines.id'), nullable=False)
    qr_code_path = db.Column(db.String(255), nullable=False)
    signature = db.Column(db.String(255), nullable=False)

    # Relationship to Invlines using back_populates
    invline = db.relationship('Invlines', back_populates='fiscal_data', lazy=True)
