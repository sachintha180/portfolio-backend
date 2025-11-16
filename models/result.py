from uuid import UUID, uuid4
from sqlmodel import Field
from sqlalchemy import CheckConstraint

from models.base import TimestampedModel


class Result(TimestampedModel, table=True):
    # Constrants
    __table_args__ = (CheckConstraint("score >= 0", name="ck_result_score_positive"),)

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    score: int = Field(nullable=False)

    # Foreign Keys
    test_id: UUID = Field(foreign_key="test.id", nullable=False)
    user_syllabus_id: UUID = Field(foreign_key="user_syllabus.id", nullable=False)
