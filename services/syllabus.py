from typing import List
from uuid import UUID
from sqlmodel import Session

from models import Syllabus

from schemas.syllabus import SyllabusCreateRequest, SyllabusUpdateRequest
from database.syllabus import SyllabusDatabase
from custom_types.exceptions import (
    SyllabusNotFoundError,
    DatabaseError,
)


class SyllabusService:
    """Service for syllabus-related business logic."""

    def __init__(self, db: SyllabusDatabase):
        """Initialize SyllabusService with a database dependency."""
        self.db = db

    def create_syllabus(
        self, db_session: Session, syllabus_data: SyllabusCreateRequest
    ) -> Syllabus:
        """Create a new syllabus."""
        try:
            syllabus = self.db.create_syllabus(db_session, syllabus_data)
        except Exception as e:
            raise DatabaseError("Failed to create syllabus") from e

        return syllabus

    def get_syllabus_by_id(self, db_session: Session, syllabus_id: UUID) -> Syllabus:
        """Get a syllabus by ID."""
        syllabus = self.db.get_syllabus_by_id(db_session, syllabus_id)
        if not syllabus:
            raise SyllabusNotFoundError

        return syllabus

    def get_all_syllabuses_by_user_id(
        self, db_session: Session, user_id: UUID
    ) -> List[Syllabus]:
        """Get all syllabuses for a user."""
        try:
            syllabuses = self.db.get_all_syllabuses_by_user_id(db_session, user_id)
        except Exception as e:
            raise DatabaseError("Failed to get syllabuses") from e

        return syllabuses

    def update_syllabus(
        self,
        db_session: Session,
        syllabus_id: UUID,
        syllabus_data: SyllabusUpdateRequest,
    ) -> Syllabus:
        """Update a syllabus with validation."""
        syllabus = self.db.get_syllabus_by_id(db_session, syllabus_id)
        if not syllabus:
            raise SyllabusNotFoundError

        try:
            updated_syllabus = self.db.update_syllabus(
                db_session, syllabus, syllabus_data
            )
        except Exception as e:
            raise DatabaseError("Failed to update syllabus") from e

        return updated_syllabus

    def delete_syllabus(self, db_session: Session, syllabus_id: UUID) -> bool:
        """Delete a syllabus."""
        syllabus = self.db.get_syllabus_by_id(db_session, syllabus_id)
        if not syllabus:
            raise SyllabusNotFoundError

        try:
            self.db.delete_syllabus(db_session, syllabus)
        except Exception as e:
            raise DatabaseError("Failed to delete syllabus") from e

        return True
