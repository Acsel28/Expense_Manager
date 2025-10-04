from pydantic import BaseModel, ConfigDict
from datetime import datetime


class CompanyBase(BaseModel):
    name: str
    currency: str = "USD"


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(CompanyBase):
    name: str | None = None
    currency: str | None = None


class CompanyResponse(CompanyBase):
    id: int
    currency: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
