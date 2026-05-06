from decimal import Decimal
from unittest import TestCase

from app.domain.entities import Company, Department, Employee, Product
from app.domain.enums import EmployeeStatus, ProductStatus
from app.domain.exceptions import DomainValidationError
from app.domain.types import Email, Sku


class CompanyTests(TestCase):
    def test_company_requires_name(self) -> None:
        with self.assertRaises(DomainValidationError):
            Company(name=" ")

    def test_company_normalizes_optional_fields(self) -> None:
        company = Company(name="  CAEP  ", tax_id="  ", description="  Holding  ")

        self.assertEqual(company.name, "CAEP")
        self.assertIsNone(company.tax_id)
        self.assertEqual(company.description, "Holding")


class DepartmentTests(TestCase):
    def test_department_belongs_to_company(self) -> None:
        company = Company(name="CAEP")
        department = Department(company_id=company.id, name="Operations")

        self.assertEqual(department.company_id, company.id)


class EmployeeTests(TestCase):
    def test_employee_normalizes_email_and_full_name(self) -> None:
        company = Company(name="CAEP")
        employee = Employee(
            company_id=company.id,
            first_name=" Ana ",
            last_name=" Torres ",
            email=Email(" ANA@EXAMPLE.COM "),
            position=" Manager ",
        )

        self.assertEqual(employee.email, "ana@example.com")
        self.assertEqual(employee.full_name, "Ana Torres")
        self.assertEqual(employee.status, EmployeeStatus.ACTIVE)

    def test_employee_requires_valid_email(self) -> None:
        company = Company(name="CAEP")

        with self.assertRaises(DomainValidationError):
            Employee(
                company_id=company.id,
                first_name="Ana",
                last_name="Torres",
                email=Email("invalid"),
                position="Manager",
            )


class ProductTests(TestCase):
    def test_product_cannot_have_negative_price(self) -> None:
        company = Company(name="CAEP")

        with self.assertRaises(DomainValidationError):
            Product(
                company_id=company.id,
                name="Platform",
                sku=Sku("PLATFORM"),
                price=Decimal("-1"),
            )

    def test_product_changes_status(self) -> None:
        company = Company(name="CAEP")
        product = Product(
            company_id=company.id,
            name="Platform",
            sku=Sku("PLATFORM"),
            price=Decimal("99.90"),
        )

        product.change_status(ProductStatus.DISCONTINUED)

        self.assertEqual(product.status, ProductStatus.DISCONTINUED)
