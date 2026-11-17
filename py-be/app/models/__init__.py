"""SQLAlchemy Models package.

IMPORTANT: Every new ORM model must be imported and re-exported here
so Alembic autogenerate can detect table schemas reliably.
"""

from app.models.base import Base, TimestampMixin

__all__ = [
    "Base",
    "TimestampMixin",
]
