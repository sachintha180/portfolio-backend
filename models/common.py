from sqlmodel import Field
from sqlalchemy import UniqueConstraint
from uuid import UUID, uuid4

from models.base import TimestampedModel


class UserSyllabus(TimestampedModel, table=True):
    # NOTE: Admins will have access to all syllabi

    # Constrants
    __table_args__ = (
        UniqueConstraint("user_id", "syllabus_id", name="uq_user_syllabus"),
    )

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", nullable=False)
    syllabus_id: UUID = Field(foreign_key="syllabus.id", nullable=False)
