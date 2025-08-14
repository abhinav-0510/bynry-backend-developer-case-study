"""
Main entry point for the StockFlow backend service.
Initializes the Flask app, sets up the database, and registers all API blueprints.
"""
from flask import Flask, jsonify
from db import db
from models import *
from routes.product_routes import product_bp
from routes.warehouse_routes import warehouse_bp
from routes.stock_transfer_routes import stock_transfer_bp
from routes.company_routes import company_bp

app = Flask(__name__)
# Configure the database URI (using SQLite for local development)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stockflow.db'
db.init_app(app)

# Register all API blueprints
app.register_blueprint(product_bp)
app.register_blueprint(warehouse_bp)
app.register_blueprint(stock_transfer_bp)
app.register_blueprint(company_bp)

@app.route('/')
def home():
    return (
        '<h1>Welcome to the StockFlow Backend API</h1>'
        '<p>Available endpoints:</p>'
        '<ul>'
        '<li>GET /api/products</li>'
        '<li>POST /api/products</li>'
        '<li>GET /api/warehouses</li>'
        '<li>POST /api/warehouses</li>'
        '<li>PUT /api/warehouses/&lt;warehouse_id&gt;</li>'
        '<li>DELETE /api/warehouses/&lt;warehouse_id&gt;</li>'
        '<li>POST /api/stock-transfer</li>'
        '</ul>'
    )

@app.route('/api/low_stock_alerts/<int:company_id>', methods=['GET'])
def low_stock_alerts(company_id):
    from models import Product
    alerts = []
    products = Product.query.filter_by(company_id=company_id).all()
    for product in products:
        threshold = product.low_stock_threshold or 10
        for inventory in product.inventories:
            if inventory.quantity < threshold:
                alerts.append({
                    'product_id': product.id,
                    'product_name': product.name,
                    'warehouse_id': inventory.warehouse_id,
                    'quantity': inventory.quantity,
                    'threshold': threshold
                })
    return jsonify(alerts)

if __name__ == '__main__':
    # Start the Flask development server
    app.run(debug=True) 