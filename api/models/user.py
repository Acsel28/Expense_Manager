from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base  # Correct relative import for database
import enum


class UserRole(str, enum.Enum):
    """Defines the roles a user can have in the system."""
    ADMIN = "admin"
    MANAGER = "manager"
    EMPLOYEE = "employee"


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.EMPLOYEE)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    # This is the foreign key column that points to the manager's ID
    manager_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True) 
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    
    # 1. Company Relationship (One-to-Many: Company has many Users)
    company = relationship("Company", back_populates="users")
    
    # 2. Manager/Subordinates Relationship (Self-Referential Many-to-One/One-to-Many)
    # 'manager' is the User object whose ID is in the current user's manager_id column
    manager = relationship(
        "User", 
        remote_side=[id],              # The column on the "remote" (manager) side
        backref="subordinates",        # Creates a 'subordinates' list on the manager User object
        foreign_keys=[manager_id]      # Explicitly states which column to use for the join
    )
    
    # 3. Expense Relationships (User submitted expenses and expenses managed by user)
    expenses = relationship("Expense", back_populates="user", foreign_keys="Expense.user_id")
    managed_expenses = relationship("Expense", back_populates="manager", foreign_keys="Expense.manager_id")
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', role='{self.role}')>"