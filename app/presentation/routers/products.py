"""Product endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import require_authenticated_user
from app.infrastructure.database.models import CompanyModel, ProductModel
from app.infrastructure.database.session import get_db_session
from app.presentation.schemas import ProductCreate, ProductRead, ProductUpdate

router = APIRouter(
    prefix="/products",
    tags=["products"],
    dependencies=[Depends(require_authenticated_user)],
)


async def _ensure_company_exists(session: AsyncSession, company_id: UUID) -> None:
    if await session.get(CompanyModel, company_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found.")


@router.get("", response_model=list[ProductRead])
async def list_products(session: AsyncSession = Depends(get_db_session)) -> list[ProductModel]:
    result = await session.execute(select(ProductModel).order_by(ProductModel.name))
    return list(result.scalars().all())


@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(
    payload: ProductCreate,
    session: AsyncSession = Depends(get_db_session),
) -> ProductModel:
    await _ensure_company_exists(session, payload.company_id)
    product = ProductModel(**payload.model_dump())
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product


@router.get("/{product_id}", response_model=ProductRead)
async def get_product(
    product_id: UUID,
    session: AsyncSession = Depends(get_db_session),
) -> ProductModel:
    product = await session.get(ProductModel, product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")
    return product


@router.patch("/{product_id}", response_model=ProductRead)
async def update_product(
    product_id: UUID,
    payload: ProductUpdate,
    session: AsyncSession = Depends(get_db_session),
) -> ProductModel:
    product = await session.get(ProductModel, product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")

    changes = payload.model_dump(exclude_unset=True)
    if "company_id" in changes:
        await _ensure_company_exists(session, changes["company_id"])

    for field, value in changes.items():
        setattr(product, field, value)

    await session.commit()
    await session.refresh(product)
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: UUID,
    session: AsyncSession = Depends(get_db_session),
) -> Response:
    product = await session.get(ProductModel, product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")

    await session.delete(product)
    await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
