"""Company entity."""

from dataclasses import dataclass, field
from datetime import datetime

from app.domain.entities._validators import optional_text, require_text
from app.domain.enums import CompanyStatus
from app.domain.types import EntityId, new_entity_id, utc_now


@dataclass(slots=True)
class Company:
    name: str
    tax_id: str | None = None
    description: str | None = None
    status: CompanyStatus = CompanyStatus.ACTIVE
    id: EntityId = field(default_factory=new_entity_id)
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        self.name = require_text(self.name, "name")
        self.tax_id = optional_text(self.tax_id)
        self.description = optional_text(self.description)

    def rename(self, name: str) -> None:
        self.name = require_text(name, "name")
        self.touch()

    def change_status(self, status: CompanyStatus) -> None:
        self.status = status
        self.touch()

    def touch(self) -> None:
        self.updated_at = utc_now()
