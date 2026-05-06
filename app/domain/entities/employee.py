"""Employee entity."""

from dataclasses import dataclass, field
from datetime import datetime

from app.domain.entities._validators import require_email, require_text
from app.domain.enums import EmployeeStatus
from app.domain.types import Email, EntityId, new_entity_id, utc_now


@dataclass(slots=True)
class Employee:
    company_id: EntityId
    first_name: str
    last_name: str
    email: Email
    position: str
    department_id: EntityId | None = None
    status: EmployeeStatus = EmployeeStatus.ACTIVE
    id: EntityId = field(default_factory=new_entity_id)
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        self.first_name = require_text(self.first_name, "first_name")
        self.last_name = require_text(self.last_name, "last_name")
        self.email = require_email(self.email)
        self.position = require_text(self.position, "position")

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def assign_department(self, department_id: EntityId | None) -> None:
        self.department_id = department_id
        self.touch()

    def change_status(self, status: EmployeeStatus) -> None:
        self.status = status
        self.touch()

    def touch(self) -> None:
        self.updated_at = utc_now()
