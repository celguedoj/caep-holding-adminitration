"""Department endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import require_authenticated_user
from app.infrastructure.database.models import CompanyModel, DepartmentModel
from app.infrastructure.database.session import get_db_session
from app.presentation.schemas import DepartmentCreate, DepartmentRead, DepartmentUpdate

router = APIRouter(
    prefix="/departments",
    tags=["departments"],
    dependencies=[Depends(require_authenticated_user)],
)


async def _ensure_company_exists(session: AsyncSession, company_id: UUID) -> None:
    if await session.get(CompanyModel, company_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found.")


@router.get("", response_model=list[DepartmentRead])
async def list_departments(
    session: AsyncSession = Depends(get_db_session),
) -> list[DepartmentModel]:
    result = await session.execute(select(DepartmentModel).order_by(DepartmentModel.name))
    return list(result.scalars().all())


@router.post("", response_model=DepartmentRead, status_code=status.HTTP_201_CREATED)
async def create_department(
    payload: DepartmentCreate,
    session: AsyncSession = Depends(get_db_session),
) -> DepartmentModel:
    await _ensure_company_exists(session, payload.company_id)
    department = DepartmentModel(**payload.model_dump())
    session.add(department)
    await session.commit()
    await session.refresh(department)
    return department


@router.get("/{department_id}", response_model=DepartmentRead)
async def get_department(
    department_id: UUID,
    session: AsyncSession = Depends(get_db_session),
) -> DepartmentModel:
    department = await session.get(DepartmentModel, department_id)
    if department is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found.")
    return department


@router.patch("/{department_id}", response_model=DepartmentRead)
async def update_department(
    department_id: UUID,
    payload: DepartmentUpdate,
    session: AsyncSession = Depends(get_db_session),
) -> DepartmentModel:
    department = await session.get(DepartmentModel, department_id)
    if department is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found.")

    changes = payload.model_dump(exclude_unset=True)
    if "company_id" in changes:
        await _ensure_company_exists(session, changes["company_id"])

    for field, value in changes.items():
        setattr(department, field, value)

    await session.commit()
    await session.refresh(department)
    return department


@router.delete("/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_department(
    department_id: UUID,
    session: AsyncSession = Depends(get_db_session),
) -> Response:
    department = await session.get(DepartmentModel, department_id)
    if department is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found.")

    await session.delete(department)
    await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
