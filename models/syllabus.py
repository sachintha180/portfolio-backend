from uuid import UUID, uuid4
from datetime import date
from sqlmodel import Field

from models.base import TimestampedModel
from custom_types.enums import SubjectCode, SyllabusLevel


class Syllabus(TimestampedModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(nullable=False)
    description: str = Field(nullable=False)
    code: SubjectCode = Field(nullable=False)
    level: SyllabusLevel = Field(nullable=False)
    examination_date: date = Field(nullable=False)
