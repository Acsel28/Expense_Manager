from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
from datetime import datetime
from api.database import get_db
from api.models.user import User, UserRole
from api.models.expense import Expense, ExpenseStatus, ExpenseCategory
from api.schemas.expense import ExpenseCreate, ExpenseResponse, ExpenseUpdate, ExpenseStatusUpdate
from api.utils.auth import get_current_user

router = APIRouter(prefix="/expenses", tags=["Expenses"])


@router.post("/", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(
    expense_data: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new expense"""
    # Create expense with current user's info
    db_expense = Expense(
        **expense_data.model_dump(),
        user_id=current_user.id,
        company_id=current_user.company_id,
        manager_id=current_user.manager_id,
        status=ExpenseStatus.PENDING
    )
    
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    
    return db_expense


@router.get("/", response_model=List[ExpenseResponse])
def list_expenses(
    skip: int = 0,
    limit: int = 100,
    status_filter: Optional[ExpenseStatus] = None,
    category_filter: Optional[ExpenseCategory] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List expenses based on user role and filters"""
    query = db.query(Expense)
    
    # Apply role-based filtering
    if current_user.role == UserRole.ADMIN:
        # Admins can see all expenses in the system
        pass
    elif current_user.role == UserRole.MANAGER:
        # Managers can see their own expenses and their subordinates' expenses
        query = query.filter(
            or_(
                Expense.user_id == current_user.id,
                Expense.manager_id == current_user.id
            )
        )
    else:
        # Employees can only see their own expenses
        query = query.filter(Expense.user_id == current_user.id)
    
    # Apply optional filters
    if status_filter:
        query = query.filter(Expense.status == status_filter)
    
    if category_filter:
        query = query.filter(Expense.category == category_filter)
    
    expenses = query.offset(skip).limit(limit).all()
    return expenses


@router.get("/pending", response_model=List[ExpenseResponse])
def list_pending_expenses(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List pending expenses that require approval (for managers)"""
    if current_user.role not in [UserRole.MANAGER, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only managers and admins can view pending approvals"
        )
    
    query = db.query(Expense).filter(Expense.status == ExpenseStatus.PENDING)
    
    if current_user.role == UserRole.MANAGER:
        # Managers only see expenses assigned to them
        query = query.filter(Expense.manager_id == current_user.id)
    
    expenses = query.offset(skip).limit(limit).all()
    return expenses


@router.get("/stats")
def get_expense_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get expense statistics for the current user"""
    from sqlalchemy import func
    
    # Base query based on role
    if current_user.role == UserRole.ADMIN:
        base_query = db.query(Expense)
    elif current_user.role == UserRole.MANAGER:
        base_query = db.query(Expense).filter(
            or_(
                Expense.user_id == current_user.id,
                Expense.manager_id == current_user.id
            )
        )
    else:
        base_query = db.query(Expense).filter(Expense.user_id == current_user.id)
    
    # Calculate statistics
    total_expenses = base_query.count()
    pending_count = base_query.filter(Expense.status == ExpenseStatus.PENDING).count()
    approved_count = base_query.filter(Expense.status == ExpenseStatus.APPROVED).count()
    rejected_count = base_query.filter(Expense.status == ExpenseStatus.REJECTED).count()
    
    total_amount = base_query.with_entities(func.sum(Expense.amount)).scalar() or 0
    approved_amount = base_query.filter(Expense.status == ExpenseStatus.APPROVED).with_entities(func.sum(Expense.amount)).scalar() or 0
    
    return {
        "total_expenses": total_expenses,
        "pending_count": pending_count,
        "approved_count": approved_count,
        "rejected_count": rejected_count,
        "total_amount": float(total_amount),
        "approved_amount": float(approved_amount)
    }


@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific expense by ID"""
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )
    
    # Check permissions
    if current_user.role == UserRole.ADMIN:
        pass  # Admins can view any expense
    elif current_user.role == UserRole.MANAGER:
        # Managers can view their own or their subordinates' expenses
        if expense.user_id != current_user.id and expense.manager_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this expense"
            )
    else:
        # Employees can only view their own expenses
        if expense.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this expense"
            )
    
    return expense


@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_expense(
    expense_id: int,
    expense_data: ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update an expense (only if pending and owned by user)"""
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )
    
    # Only the expense owner can update it
    if expense.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this expense"
        )
    
    # Can only update pending expenses
    if expense.status != ExpenseStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only update pending expenses"
        )
    
    # Update only provided fields
    update_data = expense_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(expense, field, value)
    
    db.commit()
    db.refresh(expense)
    
    return expense


@router.patch("/{expense_id}/status", response_model=ExpenseResponse)
def update_expense_status(
    expense_id: int,
    status_data: ExpenseStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Approve or reject an expense (managers only)"""
    if current_user.role not in [UserRole.MANAGER, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only managers and admins can approve/reject expenses"
        )
    
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )
    
    # Managers can only approve expenses assigned to them
    if current_user.role == UserRole.MANAGER and expense.manager_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to approve this expense"
        )
    
    # Can only approve/reject pending expenses
    if expense.status != ExpenseStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only approve/reject pending expenses"
        )
    
    # Update status and reviewed timestamp
    expense.status = status_data.status
    expense.reviewed_at = datetime.utcnow()
    
    db.commit()
    db.refresh(expense)
    
    return expense


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete an expense"""
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )
    
    # Only admins or the expense owner can delete
    if current_user.role != UserRole.ADMIN and expense.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this expense"
        )
    
    # Can only delete pending expenses
    if expense.status != ExpenseStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only delete pending expenses"
        )
    
    db.delete(expense)
    db.commit()
    
    return None
