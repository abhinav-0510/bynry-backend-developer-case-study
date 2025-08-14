from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Company(db.Model):
    """Represents a business entity using the inventory system."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)  # Company name
    warehouses = db.relationship('Warehouse', backref='company', lazy=True)
    products = db.relationship('Product', backref='company', lazy=True)

class Warehouse(db.Model):
    """A physical location where products are stored."""
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)  # Owning company
    name = db.Column(db.String(100), nullable=False)  # Warehouse name
    address = db.Column(db.String(200))  # Optional address
    inventories = db.relationship('Inventory', backref='warehouse', lazy=True)

class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    products = db.relationship('Product', secondary='supplier_product', back_populates='suppliers')

supplier_product = db.Table('supplier_product',
    db.Column('supplier_id', db.Integer, db.ForeignKey('supplier.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
)

class ProductBundle(db.Model):
    bundle_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

class InventoryChange(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventory.id'), nullable=False)
    change = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.String(100))
    changed_at = db.Column(db.DateTime, server_default=db.func.now())

# Update Product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    low_stock_threshold = db.Column(db.Integer, default=10)  # New field
    inventories = db.relationship('Inventory', backref='product', lazy=True)
    suppliers = db.relationship('Supplier', secondary='supplier_product', back_populates='products')
    is_bundle = db.Column(db.Boolean, default=False)
    bundle_items = db.relationship('ProductBundle', foreign_keys=[ProductBundle.bundle_id], backref='bundle', lazy=True)

class Inventory(db.Model):
    """Tracks the quantity of a product in a specific warehouse."""
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)  # Number of units in stock
    __table_args__ = (db.UniqueConstraint('product_id', 'warehouse_id', name='_product_warehouse_uc'),) 