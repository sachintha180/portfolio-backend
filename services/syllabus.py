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

# NOTE: In order to get back the latest data after CRUD operations, we need to refresh the session after the operation.
#       Reference: https://sqlmodel.tiangolo.com/tutorial/automatic-id-none-refresh/#refresh-objects-explicitly


class SyllabusService:
    """Service for syllabus-related business logic."""

    def __init__(self, db: SyllabusDatabase):
        """Initialize SyllabusService with a database dependency."""
        self.db = db

    def create_syllabus(
        self, db_session: Session, user_id: UUID, syllabus_data: SyllabusCreateRequest
    ) -> Syllabus:
        """Create a new syllabus and add it to the user's syllabus list."""
        try:
            syllabus = self.db.create_syllabus(db_session, syllabus_data)
            self.db.create_user_syllabus(db_session, user_id, syllabus.id)
            db_session.refresh(syllabus)
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
        """Get all syllabuses for a user, sorted by the latest created first."""
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
            db_session.refresh(updated_syllabus)
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
            db_session.refresh(syllabus)
        except Exception as e:
            raise DatabaseError("Failed to delete syllabus") from e

        return True
