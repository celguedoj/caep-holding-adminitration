"""Repository contracts owned by the domain/application boundary."""

from typing import Generic, Protocol, TypeVar

from app.domain.entities import Company, Department, Employee, Product
from app.domain.types import EntityId

EntityT = TypeVar("EntityT")


class CrudRepository(Protocol, Generic[EntityT]):
    async def get_by_id(self, entity_id: EntityId) -> EntityT | None:
        raise NotImplementedError

    async def list(self) -> list[EntityT]:
        raise NotImplementedError

    async def add(self, entity: EntityT) -> EntityT:
        raise NotImplementedError

    async def update(self, entity: EntityT) -> EntityT:
        raise NotImplementedError

    async def delete(self, entity_id: EntityId) -> None:
        raise NotImplementedError


class CompanyRepository(CrudRepository[Company], Protocol):
    async def get_by_tax_id(self, tax_id: str) -> Company | None:
        raise NotImplementedError


class DepartmentRepository(CrudRepository[Department], Protocol):
    async def list_by_company(self, company_id: EntityId) -> list[Department]:
        raise NotImplementedError


class EmployeeRepository(CrudRepository[Employee], Protocol):
    async def list_by_company(self, company_id: EntityId) -> list[Employee]:
        raise NotImplementedError

    async def list_by_department(self, department_id: EntityId) -> list[Employee]:
        raise NotImplementedError

    async def get_by_email(self, email: str) -> Employee | None:
        raise NotImplementedError


class ProductRepository(CrudRepository[Product], Protocol):
    async def list_by_company(self, company_id: EntityId) -> list[Product]:
        raise NotImplementedError

    async def get_by_sku(self, sku: str) -> Product | None:
        raise NotImplementedError
