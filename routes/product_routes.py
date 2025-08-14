from flask import Blueprint, request, jsonify
from models import db, Product, Inventory, Company, Warehouse
from sqlalchemy.exc import IntegrityError

product_bp = Blueprint('product_bp', __name__)

@product_bp.route('/api/products', methods=['POST'])
def create_product():
    data = request.get_json()
    required_fields = ['company_id', 'name', 'sku', 'price', 'warehouse_id', 'initial_quantity']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f"Please provide '{field}' in your request."}), 400
    # Validate price and quantity
    if not isinstance(data['price'], (int, float)) or data['price'] < 0:
        return jsonify({'error': 'Price must be a non-negative number.'}), 400
    if not isinstance(data['initial_quantity'], int) or data['initial_quantity'] < 0:
        return jsonify({'error': 'Initial quantity must be a non-negative integer.'}), 400
    # Enforce unique SKU
    if Product.query.filter_by(sku=data['sku']).first():
        return jsonify({'error': 'That SKU is already in use. Please choose another.'}), 400
    # Make sure the company exists
    company = Company.query.get(data['company_id'])
    if not company:
        return jsonify({'error': 'No such company found.'}), 404
    # Make sure the warehouse exists
    warehouse = Warehouse.query.get(data['warehouse_id'])
    if not warehouse:
        return jsonify({'error': 'No such warehouse found.'}), 404
    # Optional fields
    low_stock_threshold = data.get('low_stock_threshold', 10)
    # Create the product
    product = Product(
        company_id=data['company_id'],
        name=data['name'],
        sku=data['sku'],
        price=data['price'],
        low_stock_threshold=low_stock_threshold
    )
    db.session.add(product)
    db.session.flush()  # Get product.id before commit
    # Check for duplicate inventory
    if Inventory.query.filter_by(product_id=product.id, warehouse_id=data['warehouse_id']).first():
        db.session.rollback()
        return jsonify({'error': 'Inventory for this product in the warehouse already exists.'}), 400
    # Create the initial inventory record
    inventory = Inventory(
        product_id=product.id,
        warehouse_id=data['warehouse_id'],
        quantity=data['initial_quantity']
    )
    db.session.add(inventory)
    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'error': f'Something went wrong while saving the product: {str(e)}'}), 500
    return jsonify({'message': 'Product added successfully!', 'product_id': product.id}), 201

@product_bp.route('/api/products', methods=['GET'])
def list_products():
    """List all products, optionally filtered by warehouse or company."""
    warehouse_id = request.args.get('warehouse_id', type=int)
    company_id = request.args.get('company_id', type=int)
    query = Product.query
    if warehouse_id:
        query = query.join(Inventory).filter(Inventory.warehouse_id == warehouse_id)
    if company_id:
        query = query.filter(Product.company_id == company_id)
    products = query.all()
    result = []
    for p in products:
        result.append({
            'id': p.id,
            'company_id': p.company_id,
            'name': p.name,
            'sku': p.sku,
            'price': p.price,
            'warehouses': [
                {'warehouse_id': inv.warehouse_id, 'quantity': inv.quantity}
                for inv in p.inventories
            ]
        })
    return jsonify(result) 