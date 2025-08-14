from flask import Blueprint, request, jsonify
from models import db, Company
from sqlalchemy.exc import IntegrityError

company_bp = Blueprint('company_bp', __name__)

@company_bp.route('/api/companies', methods=['POST'])
def create_company():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': "Please provide 'name' in your request."}), 400
    if Company.query.filter_by(name=data['name']).first():
        return jsonify({'error': 'A company with this name already exists.'}), 400
    company = Company(name=data['name'])
    db.session.add(company)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Could not create company. Please try again.'}), 500
    return jsonify({'message': 'Company created successfully!', 'company_id': company.id}), 201

@company_bp.route('/api/companies', methods=['GET'])
def list_companies():
    companies = Company.query.all()
    return jsonify([
        {'id': c.id, 'name': c.name}
        for c in companies
    ]) 