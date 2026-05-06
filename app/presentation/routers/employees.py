"""Employee endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import require_authenticated_user
from app.infrastructure.database.models import CompanyModel, DepartmentModel, EmployeeModel
from app.infrastructure.database.session import get_db_session
from app.presentation.schemas import EmployeeCreate, EmployeeRead, EmployeeUpdate

router = APIRouter(
    prefix="/employees",
    tags=["employees"],
    dependencies=[Depends(require_authenticated_user)],
)


async def _ensure_employee_relations(
    session: AsyncSession,
    company_id: UUID | None,
    department_id: UUID | None,
) -> None:
    if company_id is not None and await session.get(CompanyModel, company_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found.")

    if department_id is not None and await session.get(DepartmentModel, department_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found.")


@router.get("", response_model=list[EmployeeRead])
async def list_employees(session: AsyncSession = Depends(get_db_session)) -> list[EmployeeModel]:
    result = await session.execute(select(EmployeeModel).order_by(EmployeeModel.last_name))
    return list(result.scalars().all())


@router.post("", response_model=EmployeeRead, status_code=status.HTTP_201_CREATED)
async def create_employee(
    payload: EmployeeCreate,
    session: AsyncSession = Depends(get_db_session),
) -> EmployeeModel:
    await _ensure_employee_relations(session, payload.company_id, payload.department_id)
    employee = EmployeeModel(**payload.model_dump())
    session.add(employee)
    await session.commit()
    await session.refresh(employee)
    return employee


@router.get("/{employee_id}", response_model=EmployeeRead)
async def get_employee(
    employee_id: UUID,
    session: AsyncSession = Depends(get_db_session),
) -> EmployeeModel:
    employee = await session.get(EmployeeModel, employee_id)
    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found.")
    return employee


@router.patch("/{employee_id}", response_model=EmployeeRead)
async def update_employee(
    employee_id: UUID,
    payload: EmployeeUpdate,
    session: AsyncSession = Depends(get_db_session),
) -> EmployeeModel:
    employee = await session.get(EmployeeModel, employee_id)
    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found.")

    changes = payload.model_dump(exclude_unset=True)
    await _ensure_employee_relations(
        session,
        changes.get("company_id"),
        changes.get("department_id"),
    )

    for field, value in changes.items():
        setattr(employee, field, value)

    await session.commit()
    await session.refresh(employee)
    return employee


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(
    employee_id: UUID,
    session: AsyncSession = Depends(get_db_session),
) -> Response:
    employee = await session.get(EmployeeModel, employee_id)
    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found.")

    await session.delete(employee)
    await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
