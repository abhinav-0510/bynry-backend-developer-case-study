from flask import Blueprint, request, jsonify
from models import db, Inventory
from sqlalchemy.exc import IntegrityError

stock_transfer_bp = Blueprint('stock_transfer_bp', __name__)

@stock_transfer_bp.route('/api/stock-transfer', methods=['POST'])
def stock_transfer():
    """Transfer stock of a product from one warehouse to another."""
    data = request.get_json()
    required_fields = ['product_id', 'from_warehouse_id', 'to_warehouse_id', 'quantity']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f"Missing required field: '{field}'."}), 400
    if data['from_warehouse_id'] == data['to_warehouse_id']:
        return jsonify({'error': 'Source and destination warehouses must be different.'}), 400
    if data['quantity'] <= 0:
        return jsonify({'error': 'Quantity must be a positive number.'}), 400
    # Find the inventory record for the source warehouse
    source_inv = Inventory.query.filter_by(product_id=data['product_id'], warehouse_id=data['from_warehouse_id']).first()
    if not source_inv or source_inv.quantity < data['quantity']:
        return jsonify({'error': 'Not enough stock in the source warehouse to complete this transfer.'}), 400
    # Find or create the inventory record for the destination warehouse
    dest_inv = Inventory.query.filter_by(product_id=data['product_id'], warehouse_id=data['to_warehouse_id']).first()
    if not dest_inv:
        dest_inv = Inventory(product_id=data['product_id'], warehouse_id=data['to_warehouse_id'], quantity=0)
        db.session.add(dest_inv)
    # Perform the stock transfer
    source_inv.quantity -= data['quantity']
    dest_inv.quantity += data['quantity']
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Could not complete the stock transfer. Please try again.'}), 500
    return jsonify({'message': 'Stock transferred successfully.'}) 