"""Domain enumerations."""

from enum import StrEnum


class CompanyStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class EmployeeStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ON_LEAVE = "on_leave"


class ProductStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DISCONTINUED = "discontinued"
