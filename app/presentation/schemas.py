"""API schemas."""

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.domain.enums import CompanyStatus, EmployeeStatus, ProductStatus


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    username: str
    password: str


class CompanyCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    tax_id: str | None = Field(default=None, max_length=80)
    description: str | None = None
    status: CompanyStatus = CompanyStatus.ACTIVE


class CompanyUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=150)
    tax_id: str | None = Field(default=None, max_length=80)
    description: str | None = None
    status: CompanyStatus | None = None


class CompanyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    tax_id: str | None
    description: str | None
    status: CompanyStatus
    created_at: datetime
    updated_at: datetime


class DepartmentCreate(BaseModel):
    company_id: UUID
    name: str = Field(min_length=1, max_length=150)
    description: str | None = None


class DepartmentUpdate(BaseModel):
    company_id: UUID | None = None
    name: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = None


class DepartmentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    company_id: UUID
    name: str
    description: str | None
    created_at: datetime
    updated_at: datetime


class EmployeeCreate(BaseModel):
    company_id: UUID
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    position: str = Field(min_length=1, max_length=120)
    department_id: UUID | None = None
    status: EmployeeStatus = EmployeeStatus.ACTIVE


class EmployeeUpdate(BaseModel):
    company_id: UUID | None = None
    department_id: UUID | None = None
    first_name: str | None = Field(default=None, min_length=1, max_length=100)
    last_name: str | None = Field(default=None, min_length=1, max_length=100)
    email: EmailStr | None = None
    position: str | None = Field(default=None, min_length=1, max_length=120)
    status: EmployeeStatus | None = None


class EmployeeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    company_id: UUID
    department_id: UUID | None
    first_name: str
    last_name: str
    email: str
    position: str
    status: EmployeeStatus
    created_at: datetime
    updated_at: datetime


class ProductCreate(BaseModel):
    company_id: UUID
    name: str = Field(min_length=1, max_length=150)
    sku: str = Field(min_length=1, max_length=80)
    price: Decimal = Field(ge=0)
    description: str | None = None
    status: ProductStatus = ProductStatus.ACTIVE


class ProductUpdate(BaseModel):
    company_id: UUID | None = None
    name: str | None = Field(default=None, min_length=1, max_length=150)
    sku: str | None = Field(default=None, min_length=1, max_length=80)
    price: Decimal | None = Field(default=None, ge=0)
    description: str | None = None
    status: ProductStatus | None = None


class ProductRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    company_id: UUID
    name: str
    sku: str
    price: Decimal
    description: str | None
    status: ProductStatus
    created_at: datetime
    updated_at: datetime
