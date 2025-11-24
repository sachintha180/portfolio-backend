from datetime import datetime, date
from typing import List, Optional
from uuid import UUID, uuid4
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import DateTime, func, UniqueConstraint, CheckConstraint
from pydantic import EmailStr

from custom_types.enums import UserType, SubjectCode, SyllabusLevel, FileType

# NOTE: The following are the established cascade deletes:
# - Deleting user_syllabus -> deletes associated results
# - Deleting syllabus -> deletes associated lessons and tests
# - Deleting lesson -> deletes associated files
# - Deleting test -> deletes associated results


# NOTE: If you use sa_column here, created_at/updated_at columns will be instantiated and
#       then SQLAlchemy will try to set the same column to several tables which is not allowed.
class TimestampedModel(SQLModel):
    created_at: Optional[datetime] = Field(
        default=None,
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={
            "server_default": func.now(),
            "nullable": False,
        },
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={
            "server_default": func.now(),
            "onupdate": func.now(),
            "nullable": False,
        },
    )


class UserSyllabus(TimestampedModel, table=True):
    __tablename__: str = (
        "user_syllabus"  # NOTE: To prevent the default name, which is "usersyllabus"
    )

    # Constrants
    __table_args__ = (
        UniqueConstraint("user_id", "syllabus_id", name="uq_user_syllabus"),
    )

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", nullable=False)
    syllabus_id: UUID = Field(foreign_key="syllabus.id", nullable=False)

    # Relationships
    results: List["Result"] = Relationship(
        back_populates="user_syllabus", cascade_delete=True
    )


class User(TimestampedModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    first_name: str = Field(nullable=False, max_length=100)
    last_name: str = Field(nullable=False, max_length=100)
    email: EmailStr = Field(unique=True, index=True)
    password: str = Field(nullable=False)
    type: UserType = Field(nullable=False, index=True)

    # Relationships
    syllabuses: List["Syllabus"] = Relationship(
        back_populates="users", link_model=UserSyllabus
    )


class Syllabus(TimestampedModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(nullable=False)
    description: str = Field(nullable=False)
    code: SubjectCode = Field(nullable=False)
    level: SyllabusLevel = Field(nullable=False)
    examination_date: date = Field(nullable=False)

    # Relationships
    users: List["User"] = Relationship(
        back_populates="syllabuses", link_model=UserSyllabus
    )

    lessons: List["Lesson"] = Relationship(
        back_populates="syllabus", cascade_delete=True
    )

    tests: List["Test"] = Relationship(back_populates="syllabus", cascade_delete=True)


class Lesson(TimestampedModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(nullable=False)
    description: str = Field(nullable=False)
    conducted_at: date = Field(nullable=False, index=True)

    # Relationships
    syllabus_id: UUID = Field(foreign_key="syllabus.id", nullable=False)
    syllabus: "Syllabus" = Relationship(back_populates="lessons")

    files: List["File"] = Relationship(back_populates="lesson", cascade_delete=True)


class File(TimestampedModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(nullable=False)
    description: str = Field(nullable=False)
    filename: str = Field(nullable=False, max_length=255)
    gdrive_url: str = Field(nullable=False, max_length=2048)
    completed: bool = Field(default=False)
    type: FileType = Field(nullable=False)

    # Relationships
    lesson_id: UUID = Field(foreign_key="lesson.id", nullable=False)
    lesson: "Lesson" = Relationship(back_populates="files")


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

    # Relationships
    syllabus_id: UUID = Field(foreign_key="syllabus.id", nullable=False)
    syllabus: "Syllabus" = Relationship(back_populates="tests")

    results: List["Result"] = Relationship(back_populates="test", cascade_delete=True)


class Result(TimestampedModel, table=True):
    # Constrants
    __table_args__ = (CheckConstraint("score >= 0", name="ck_result_score_positive"),)

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    score: int = Field(nullable=False)

    # Relationships
    test_id: UUID = Field(foreign_key="test.id", nullable=False)
    test: "Test" = Relationship(back_populates="results")

    user_syllabus_id: UUID = Field(foreign_key="user_syllabus.id", nullable=False)
    user_syllabus: "UserSyllabus" = Relationship(back_populates="results")
