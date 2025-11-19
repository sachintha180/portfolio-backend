from uuid import UUID, uuid4
from datetime import date
from sqlmodel import Field
from sqlalchemy import CheckConstraint

from models.base import TimestampedModel


class Test(TimestampedModel, table=True):
    # Constrants
    __table_args__ = (
        CheckConstraint("total_marks >= 0", name="ck_test_total_marks_positive"),
        CheckConstraint("duration >= 0", name="ck_test_duration_positive"),
    )

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(nullable=False)
    description: str = Field(nullable=False)
    total_marks: int = Field(nullable=False)
    duration: int = Field(nullable=False)
    conducted_at: date = Field(nullable=False, index=True)

    # Foreign Keys
    syllabus_id: UUID = Field(foreign_key="syllabus.id", nullable=False)
