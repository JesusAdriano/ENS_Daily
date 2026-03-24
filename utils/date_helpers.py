from datetime import date
from typing import Optional


def serialize_date(value: Optional[date]) -> Optional[str]:
    return value.isoformat() if value else None


def deserialize_date(value: Optional[str]) -> Optional[date]:
    return date.fromisoformat(value) if value else None
