from uuid import UUID, uuid4
from datetime import date
from sqlmodel import Field
from pydantic import EmailStr
from sqlalchemy import CheckConstraint, UniqueConstraint

from models.base import TimestampedModel
from custom_types.enums import UserType, SubjectCode, SyllabusLevel, FileType


class User(TimestampedModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    first_name: str = Field(nullable=False, max_length=100)
    last_name: str = Field(nullable=False, max_length=100)
    email: EmailStr = Field(unique=True, index=True)
    password: str = Field(nullable=False)
    type: UserType = Field(nullable=False, index=True)


class Syllabus(TimestampedModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(nullable=False)
    description: str = Field(nullable=False)
    code: SubjectCode = Field(nullable=False)
    level: SyllabusLevel = Field(nullable=False)
    examination_date: date = Field(nullable=False)


class UserSyllabus(TimestampedModel, table=True):
    # NOTE: Admins will have access to all syllabi

    # Constrants
    __table_args__ = (
        UniqueConstraint("user_id", "syllabus_id", name="uq_user_syllabus"),
    )

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", nullable=False)
    syllabus_id: UUID = Field(foreign_key="syllabus.id", nullable=False)


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


class Result(TimestampedModel, table=True):
    # Constrants
    __table_args__ = (CheckConstraint("score >= 0", name="ck_result_score_positive"),)

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    score: int = Field(nullable=False)

    # Foreign Keys
    test_id: UUID = Field(foreign_key="test.id", nullable=False)
    user_syllabus_id: UUID = Field(foreign_key="user_syllabus.id", nullable=False)


class Lesson(TimestampedModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(nullable=False)
    description: str = Field(nullable=False)
    conducted_at: date = Field(nullable=False, index=True)

    # Foreign Keys
    syllabus_id: UUID = Field(foreign_key="syllabus.id", nullable=False)


class File(TimestampedModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(nullable=False)
    description: str = Field(nullable=False)
    filename: str = Field(nullable=False, max_length=255)
    gdrive_url: str = Field(nullable=False, max_length=2048)
    completed: bool = Field(default=False)
    type: FileType = Field(nullable=False)

    # Foreign Keys
    lesson_id: UUID = Field(foreign_key="lesson.id", nullable=False)
