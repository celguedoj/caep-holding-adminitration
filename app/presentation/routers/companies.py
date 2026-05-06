"""Company endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import require_authenticated_user
from app.infrastructure.database.models import (
    CompanyModel,
    DepartmentModel,
    EmployeeModel,
    ProductModel,
)
from app.infrastructure.database.session import get_db_session
from app.presentation.schemas import (
    CompanyCreate,
    CompanyRead,
    CompanyUpdate,
    DepartmentRead,
    EmployeeRead,
    ProductRead,
)

router = APIRouter(tags=["companies"])
protected_router = APIRouter(
    prefix="/companies",
    tags=["companies"],
    dependencies=[Depends(require_authenticated_user)],
)


@router.get("/public/companies", response_model=list[CompanyRead])
async def list_public_companies(
    session: AsyncSession = Depends(get_db_session),
) -> list[CompanyModel]:
    result = await session.execute(select(CompanyModel).order_by(CompanyModel.name))
    return list(result.scalars().all())


@protected_router.get("", response_model=list[CompanyRead])
async def list_companies(session: AsyncSession = Depends(get_db_session)) -> list[CompanyModel]:
    result = await session.execute(select(CompanyModel).order_by(CompanyModel.name))
    return list(result.scalars().all())


@protected_router.post("", response_model=CompanyRead, status_code=status.HTTP_201_CREATED)
async def create_company(
    payload: CompanyCreate,
    session: AsyncSession = Depends(get_db_session),
) -> CompanyModel:
    company = CompanyModel(**payload.model_dump())
    session.add(company)
    await session.commit()
    await session.refresh(company)
    return company


@protected_router.get("/{company_id}", response_model=CompanyRead)
async def get_company(
    company_id: UUID,
    session: AsyncSession = Depends(get_db_session),
) -> CompanyModel:
    company = await session.get(CompanyModel, company_id)
    if company is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found.")
    return company


@protected_router.get("/{company_id}/departments", response_model=list[DepartmentRead])
async def list_company_departments(
    company_id: UUID,
    session: AsyncSession = Depends(get_db_session),
) -> list[DepartmentModel]:
    await _ensure_company_exists(session, company_id)
    result = await session.execute(
        select(DepartmentModel)
        .where(DepartmentModel.company_id == company_id)
        .order_by(DepartmentModel.name)
    )
    return list(result.scalars().all())


@protected_router.get("/{company_id}/products", response_model=list[ProductRead])
async def list_company_products(
    company_id: UUID,
    session: AsyncSession = Depends(get_db_session),
) -> list[ProductModel]:
    await _ensure_company_exists(session, company_id)
    result = await session.execute(
        select(ProductModel)
        .where(ProductModel.company_id == company_id)
        .order_by(ProductModel.name)
    )
    return list(result.scalars().all())


@protected_router.get("/{company_id}/employees", response_model=list[EmployeeRead])
async def list_company_employees(
    company_id: UUID,
    session: AsyncSession = Depends(get_db_session),
) -> list[EmployeeModel]:
    await _ensure_company_exists(session, company_id)
    result = await session.execute(
        select(EmployeeModel)
        .where(EmployeeModel.company_id == company_id)
        .order_by(EmployeeModel.last_name, EmployeeModel.first_name)
    )
    return list(result.scalars().all())


@protected_router.patch("/{company_id}", response_model=CompanyRead)
async def update_company(
    company_id: UUID,
    payload: CompanyUpdate,
    session: AsyncSession = Depends(get_db_session),
) -> CompanyModel:
    company = await session.get(CompanyModel, company_id)
    if company is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found.")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(company, field, value)

    await session.commit()
    await session.refresh(company)
    return company


@protected_router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(
    company_id: UUID,
    session: AsyncSession = Depends(get_db_session),
) -> Response:
    company = await session.get(CompanyModel, company_id)
    if company is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found.")

    await session.delete(company)
    await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


async def _ensure_company_exists(session: AsyncSession, company_id: UUID) -> None:
    if await session.get(CompanyModel, company_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found.")
