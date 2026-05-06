"""Product entity."""

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal

from app.domain.entities._validators import optional_text, require_text
from app.domain.enums import ProductStatus
from app.domain.exceptions import DomainValidationError
from app.domain.types import EntityId, Sku, new_entity_id, utc_now


@dataclass(slots=True)
class Product:
    company_id: EntityId
    name: str
    sku: Sku
    price: Decimal
    description: str | None = None
    status: ProductStatus = ProductStatus.ACTIVE
    id: EntityId = field(default_factory=new_entity_id)
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        self.name = require_text(self.name, "name")
        self.sku = Sku(require_text(str(self.sku), "sku"))
        self.description = optional_text(self.description)
        if self.price < Decimal("0"):
            raise DomainValidationError("price cannot be negative.")

    def change_price(self, price: Decimal) -> None:
        if price < Decimal("0"):
            raise DomainValidationError("price cannot be negative.")
        self.price = price
        self.touch()

    def change_status(self, status: ProductStatus) -> None:
        self.status = status
        self.touch()

    def touch(self) -> None:
        self.updated_at = utc_now()
