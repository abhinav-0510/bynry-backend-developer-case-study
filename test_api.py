import requests

BASE_URL = 'http://localhost:5000'

# 1. Add a company (if endpoint exists, otherwise skip)
def add_company():
    url = f'{BASE_URL}/api/companies'
    data = {"name": "Test Company"}
    try:
        r = requests.post(url, json=data)
        print('Add company:', r.status_code, r.json())
        return r.json().get('company_id', 1)  # fallback to 1 if not returned
    except Exception as e:
        print('Add company failed:', e)
        return 1

# 2. Add a warehouse
def add_warehouse(company_id):
    url = f'{BASE_URL}/api/warehouses'
    data = {"company_id": company_id, "name": "Main Warehouse"}
    r = requests.post(url, json=data)
    print('Add warehouse:', r.status_code, r.json())
    return r.json().get('warehouse_id', 1)

# 3. Add a product
def add_product(company_id, warehouse_id):
    url = f'{BASE_URL}/api/products'
    data = {
        "company_id": company_id,
        "name": "Widget",
        "sku": "WGT-001",
        "price": 10.5,
        "warehouse_id": warehouse_id,
        "initial_quantity": 5,
        "low_stock_threshold": 10
    }
    r = requests.post(url, json=data)
    print('Add product:', r.status_code, r.json())
    return r.json().get('product_id', 1)

# 4. Get low stock alerts
def get_low_stock_alerts(company_id):
    url = f'{BASE_URL}/api/low_stock_alerts/{company_id}'
    r = requests.get(url)
    print('Low stock alerts:', r.status_code, r.json())

if __name__ == '__main__':
    # If you have /api/companies, use it, else set company_id = 1
    company_id = 1
    # company_id = add_company()  # Uncomment if /api/companies exists
    warehouse_id = add_warehouse(company_id)
    product_id = add_product(company_id, warehouse_id)
    get_low_stock_alerts(company_id) 