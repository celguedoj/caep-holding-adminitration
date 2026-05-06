"""Company endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import require_authenticated_user
from app.infrastructure.database.models import CompanyModel
from app.infrastructure.database.session import get_db_session
from app.presentation.schemas import CompanyCreate, CompanyRead, CompanyUpdate

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
