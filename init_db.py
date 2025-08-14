"""
Database initialization script for StockFlow.
Run this script to create all tables in your local development database.
"""
from app import app, db

def init_db():
    """Create all database tables defined in the models."""
    with app.app_context():
        db.create_all()
        print('Database initialized successfully.')

if __name__ == '__main__':
    # Run this script directly to set up the database
    init_db() 