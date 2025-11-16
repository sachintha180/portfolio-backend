from uuid import UUID, uuid4
from datetime import date
from sqlmodel import Field

from models.base import TimestampedModel


class Lesson(TimestampedModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(nullable=False)
    description: str = Field(nullable=False)
    conducted_at: date = Field(nullable=False, index=True)

    # Foreign Keys
    syllabus_id: UUID = Field(foreign_key="syllabus.id", nullable=False)
