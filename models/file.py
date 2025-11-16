from uuid import UUID, uuid4
from sqlmodel import Field

from models.base import TimestampedModel
from custom_types.enums import FileType


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
