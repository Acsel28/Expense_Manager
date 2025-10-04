from pydantic import BaseModel, ConfigDict
from datetime import datetime
from ..models.expense import ExpenseStatus, ExpenseCategory
from decimal import Decimal
from typing import Optional


class ExpenseBase(BaseModel):
    title: str
    amount: Decimal
    category: ExpenseCategory
    description: Optional[str] = None
    receipt_url: Optional[str] = None


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(BaseModel):
    title: str | None = None
    amount: Decimal | None = None
    category: ExpenseCategory | None = None
    description: str | None = None
    receipt_url: str | None = None


class ExpenseStatusUpdate(BaseModel):
    status: ExpenseStatus


class ExpenseResponse(ExpenseBase):
    id: int
    status: ExpenseStatus
    user_id: int
    company_id: int
    manager_id: Optional[int] = None
    submitted_at: datetime
    reviewed_at: Optional[datetime] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
