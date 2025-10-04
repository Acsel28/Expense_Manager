from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base
import enum


class ExpenseStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class ExpenseCategory(str, enum.Enum):
    TRAVEL = "travel"
    MEALS = "meals"
    OFFICE = "office"
    EQUIPMENT = "equipment"
    SOFTWARE = "software"
    OTHER = "other"


class Expense(Base):
    __tablename__ = "expenses"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    category = Column(SQLEnum(ExpenseCategory), nullable=False)
    description = Column(Text, nullable=True)
    receipt_url = Column(String, nullable=True)
    status = Column(SQLEnum(ExpenseStatus), nullable=False, default=ExpenseStatus.PENDING)
    
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    manager_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    submitted_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="expenses", foreign_keys=[user_id])
    company = relationship("Company", back_populates="expenses")
    manager = relationship("User", back_populates="managed_expenses", foreign_keys=[manager_id])
    
    def __repr__(self):
        return f"<Expense(id={self.id}, title='{self.title}', amount={self.amount}, status='{self.status}')>"
