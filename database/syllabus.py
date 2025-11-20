from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select

from models import UserSyllabus, Syllabus
from schemas.syllabus import SyllabusCreateRequest, SyllabusUpdateRequest


class SyllabusDatabase:
    """Database layer for syllabus operations."""

    def create_syllabus(
        self, db_session: Session, syllabus_data: SyllabusCreateRequest
    ) -> Syllabus:
        """Create a new syllabus in the database."""
        syllabus = Syllabus(**syllabus_data.model_dump())
        db_session.add(syllabus)
        db_session.commit()
        db_session.refresh(syllabus)
        return syllabus

    def get_syllabus_by_id(
        self, db_session: Session, syllabus_id: UUID
    ) -> Optional[Syllabus]:
        """Get a syllabus by ID."""
        statement = select(Syllabus).where(Syllabus.id == syllabus_id)
        return db_session.exec(statement).first()

    def get_all_syllabuses_by_user_id(
        self, db_session: Session, user_id: UUID
    ) -> List[Syllabus]:
        """Get all syllabuses for a user."""
        statement = (
            select(Syllabus).join(UserSyllabus).where(UserSyllabus.user_id == user_id)
        )
        return list(db_session.exec(statement).all())

    def update_syllabus(
        self,
        db_session: Session,
        syllabus: Syllabus,
        syllabus_data: SyllabusUpdateRequest,
    ) -> Syllabus:
        """Update a syllabus in the database."""
        update_dict = syllabus_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(syllabus, key, value)

        db_session.add(syllabus)
        db_session.commit()
        db_session.refresh(syllabus)
        return syllabus

    def delete_syllabus(self, db_session: Session, syllabus: Syllabus) -> bool:
        """Delete a syllabus from the database."""
        db_session.delete(syllabus)
        db_session.commit()
        return True
