"""Shared domain types."""

from datetime import datetime, timezone
from typing import NewType
from uuid import UUID, uuid4

EntityId = NewType("EntityId", UUID)
Email = NewType("Email", str)
Sku = NewType("Sku", str)


def new_entity_id() -> EntityId:
    return EntityId(uuid4())


def utc_now() -> datetime:
    return datetime.now(timezone.utc)
