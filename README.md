# StockFlow Backend

StockFlow is a B2B inventory management platform designed for small businesses to track products across multiple warehouses and manage supplier relationships.

## Features
- Manage companies, warehouses, and products
- Track inventory across multiple warehouses
- Transfer stock between warehouses
- RESTful API endpoints for all core operations

## Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Setup
1. Clone this repository or download the source code.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Initialize the database:
   ```bash
   python init_db.py
   ```
4. Start the development server:
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5000/` by default.

## API Overview
- `POST /api/products` — Add a new product
- `GET /api/products` — List products (filter by company or warehouse)
- `POST /api/warehouses` — Create a warehouse
- `GET /api/warehouses` — List warehouses (filter by company)
- `POST /api/stock-transfer` — Transfer stock between warehouses

See the code for full details on request/response formats.

## Notes
- This project uses SQLite for local development. For production, update the database URI in `app.py`.
- All error messages and responses are designed to be clear and helpful.
- Contributions and suggestions are welcome!

---

*Developed as part of a backend engineering case study.* 