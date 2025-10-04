"""
Simple database initialization script for uvicorn
"""
import sys
import os
from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base
from models import Company, User, Expense
from models.user import UserRole
from models.expense import ExpenseStatus, ExpenseCategory
from utils.auth import get_password_hash
from decimal import Decimal


def create_tables():
    """Create all database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tables created successfully")


def seed_data():
    """Seed initial data for testing"""
    db = SessionLocal()
    
    try:
        print("\nSeeding initial data...")
        
        # Create company
        company = Company(name="Acme Corporation")
        db.add(company)
        db.commit()
        db.refresh(company)
        print(f"✓ Created company: {company.name}")
        
        # Create admin user
        admin = User(
            email="admin@acme.com",
            hashed_password=get_password_hash("admin123"),
            full_name="Admin User",
            role=UserRole.ADMIN,
            company_id=company.id
        )
        
        # Create manager user
        manager = User(
            email="manager@acme.com",
            hashed_password=get_password_hash("manager123"),
            full_name="John Manager",
            role=UserRole.MANAGER,
            company_id=company.id
        )
        
        db.add_all([admin, manager])
        db.commit()
        db.refresh(manager)
        
        # Create employee user
        employee = User(
            email="alice@acme.com",
            hashed_password=get_password_hash("alice123"),
            full_name="Alice Employee",
            role=UserRole.EMPLOYEE,
            company_id=company.id,
            manager_id=manager.id
        )
        
        db.add(employee)
        db.commit()
        db.refresh(employee)
        
        print(f"✓ Created users:")
        print(f"  - Admin: admin@acme.com (password: admin123)")
        print(f"  - Manager: manager@acme.com (password: manager123)")
        print(f"  - Employee: alice@acme.com (password: alice123)")
        
        # Create sample expenses
        expense1 = Expense(
            title="Client Lunch Meeting",
            amount=Decimal("125.50"),
            category=ExpenseCategory.MEALS,
            description="Lunch with potential client",
            status=ExpenseStatus.PENDING,
            user_id=employee.id,
            company_id=company.id,
            manager_id=manager.id
        )
        
        expense2 = Expense(
            title="Conference Travel",
            amount=Decimal("850.00"),
            category=ExpenseCategory.TRAVEL,
            description="Flight tickets for tech conference",
            status=ExpenseStatus.APPROVED,
            user_id=employee.id,
            company_id=company.id,
            manager_id=manager.id
        )
        
        db.add_all([expense1, expense2])
        db.commit()
        
        print(f"✓ Created 2 sample expenses")
        print("\n✓ Database seeded successfully!")
        
    except Exception as e:
        print(f"✗ Error seeding data: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def main():
    """Main initialization function"""
    print("=" * 50)
    print("ExesMan Database Initialization")
    print("=" * 50)
    
    try:
        create_tables()
        seed_data()
        
        print("\n" + "=" * 50)
        print("Database initialization complete!")
        print("=" * 50)
        print("\nYou can now start the API server with:")
        print("  uvicorn main:app --reload --host 0.0.0.0 --port 8000")
        
    except Exception as e:
        print(f"\n✗ Initialization failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()


