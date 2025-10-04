"""
Database initialization script
Creates all tables and seeds initial data
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sqlalchemy.orm import Session
from api.database import engine, SessionLocal, Base
from api.models import Company, User, Expense
from api.models.user import UserRole
from api.models.expense import ExpenseStatus, ExpenseCategory
from api.utils.auth import get_password_hash
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
        
        # Create companies
        company1 = Company(name="Acme Corporation")
        company2 = Company(name="TechStart Inc")
        
        db.add_all([company1, company2])
        db.commit()
        db.refresh(company1)
        db.refresh(company2)
        print(f"✓ Created companies: {company1.name}, {company2.name}")
        
        # Create users
        # Admin user
        admin = User(
            email="admin@acme.com",
            hashed_password=get_password_hash("admin123"),
            full_name="Admin User",
            role=UserRole.ADMIN,
            company_id=company1.id
        )
        
        # Manager user
        manager = User(
            email="manager@acme.com",
            hashed_password=get_password_hash("manager123"),
            full_name="John Manager",
            role=UserRole.MANAGER,
            company_id=company1.id
        )
        
        db.add_all([admin, manager])
        db.commit()
        db.refresh(manager)
        
        # Employee users
        employee1 = User(
            email="alice@acme.com",
            hashed_password=get_password_hash("alice123"),
            full_name="Alice Employee",
            role=UserRole.EMPLOYEE,
            company_id=company1.id,
            manager_id=manager.id
        )
        
        employee2 = User(
            email="bob@acme.com",
            hashed_password=get_password_hash("bob123"),
            full_name="Bob Employee",
            role=UserRole.EMPLOYEE,
            company_id=company1.id,
            manager_id=manager.id
        )
        
        db.add_all([employee1, employee2])
        db.commit()
        db.refresh(employee1)
        db.refresh(employee2)
        
        print(f"✓ Created users:")
        print(f"  - Admin: admin@acme.com (password: admin123)")
        print(f"  - Manager: manager@acme.com (password: manager123)")
        print(f"  - Employee: alice@acme.com (password: alice123)")
        print(f"  - Employee: bob@acme.com (password: bob123)")
        
        # Create sample expenses
        expense1 = Expense(
            title="Client Lunch Meeting",
            amount=Decimal("125.50"),
            category=ExpenseCategory.MEALS,
            description="Lunch with potential client at downtown restaurant",
            status=ExpenseStatus.PENDING,
            user_id=employee1.id,
            company_id=company1.id,
            manager_id=manager.id
        )
        
        expense2 = Expense(
            title="Conference Travel",
            amount=Decimal("850.00"),
            category=ExpenseCategory.TRAVEL,
            description="Flight tickets for tech conference",
            status=ExpenseStatus.APPROVED,
            user_id=employee1.id,
            company_id=company1.id,
            manager_id=manager.id
        )
        
        expense3 = Expense(
            title="Office Supplies",
            amount=Decimal("45.99"),
            category=ExpenseCategory.OFFICE,
            description="Notebooks and pens",
            status=ExpenseStatus.PENDING,
            user_id=employee2.id,
            company_id=company1.id,
            manager_id=manager.id
        )
        
        db.add_all([expense1, expense2, expense3])
        db.commit()
        
        print(f"✓ Created {3} sample expenses")
        
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
        print("  python main.py")
        print("\nOr use uvicorn:")
        print("  uvicorn main:app --reload")
        
    except Exception as e:
        print(f"\n✗ Initialization failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
