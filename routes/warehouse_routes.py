from flask import Blueprint, request, jsonify
from models import db, Warehouse, Company
from sqlalchemy.exc import IntegrityError

warehouse_bp = Blueprint('warehouse_bp', __name__)

@warehouse_bp.route('/api/warehouses', methods=['POST'])
def create_warehouse():
    """Create a new warehouse for a company."""
    data = request.get_json()
    required_fields = ['company_id', 'name']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f"Missing required field: '{field}'."}), 400
    # Make sure the company exists
    company = Company.query.get(data['company_id'])
    if not company:
        return jsonify({'error': 'Company not found. Please check the company ID.'}), 404
    warehouse = Warehouse(
        company_id=data['company_id'],
        name=data['name'],
        address=data.get('address')
    )
    db.session.add(warehouse)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Could not save the warehouse. Please try again.'}), 500
    return jsonify({'message': 'Warehouse created successfully!', 'warehouse_id': warehouse.id}), 201

@warehouse_bp.route('/api/warehouses', methods=['GET'])
def list_warehouses():
    """List all warehouses, optionally filtered by company."""
    company_id = request.args.get('company_id', type=int)
    query = Warehouse.query
    if company_id:
        query = query.filter_by(company_id=company_id)
    warehouses = query.all()
    return jsonify([
        {
            'id': w.id,
            'company_id': w.company_id,
            'name': w.name,
            'address': w.address
        } for w in warehouses
    ])

@warehouse_bp.route('/api/warehouses/<int:warehouse_id>', methods=['PUT'])
def update_warehouse(warehouse_id):
    """Update the details of an existing warehouse."""
    warehouse = Warehouse.query.get_or_404(warehouse_id)
    data = request.get_json()
    if 'name' in data:
        warehouse.name = data['name']
    if 'address' in data:
        warehouse.address = data['address']
    db.session.commit()
    return jsonify({'message': 'Warehouse updated.'})

@warehouse_bp.route('/api/warehouses/<int:warehouse_id>', methods=['DELETE'])
def delete_warehouse(warehouse_id):
    """Delete a warehouse from the system."""
    warehouse = Warehouse.query.get_or_404(warehouse_id)
    db.session.delete(warehouse)
    db.session.commit()
    return jsonify({'message': 'Warehouse deleted.'}) 