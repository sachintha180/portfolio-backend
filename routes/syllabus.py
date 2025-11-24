from uuid import UUID
from fastapi import APIRouter, status

from schemas.syllabus import (
    SyllabusCreateRequest,
    SyllabusCreateResponse,
    SyllabusGetResponse,
    SyllabusesGetResponse,
    SyllabusUpdateRequest,
    SyllabusUpdateResponse,
)
from custom_types.dependencies import (
    AuthenticatedUserDep,
    DBSessionDep,
    SyllabusServiceDep,
)

router = APIRouter(prefix="/syllabus", tags=["syllabus"])


@router.post(
    "/",
    response_model=SyllabusCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_syllabus(
    request_data: SyllabusCreateRequest,
    authenticated_user: AuthenticatedUserDep,
    syllabus_service: SyllabusServiceDep,
    db_session: DBSessionDep,
):
    """Create a new syllabus."""
    user_id = authenticated_user.id
    syllabus = syllabus_service.create_syllabus(db_session, user_id, request_data)

    return SyllabusCreateResponse(syllabus=syllabus)


@router.get(
    "/all",
    response_model=SyllabusesGetResponse,
    status_code=status.HTTP_200_OK,
)
def get_syllabuses(
    authenticated_user: AuthenticatedUserDep,
    syllabus_service: SyllabusServiceDep,
    db_session: DBSessionDep,
):
    """Get all syllabuses."""
    user_id = authenticated_user.id
    syllabuses = syllabus_service.get_all_syllabuses_by_user_id(db_session, user_id)

    return SyllabusesGetResponse(syllabuses=syllabuses)


@router.get(
    "/{syllabus_id}",
    response_model=SyllabusGetResponse,
    status_code=status.HTTP_200_OK,
)
def get_syllabus(
    syllabus_id: UUID,
    _: AuthenticatedUserDep,
    syllabus_service: SyllabusServiceDep,
    db_session: DBSessionDep,
):
    """Get a syllabus by ID."""
    syllabus = syllabus_service.get_syllabus_by_id(db_session, syllabus_id)

    return SyllabusGetResponse(syllabus=syllabus)


@router.patch(
    "/{syllabus_id}",
    response_model=SyllabusUpdateResponse,
    status_code=status.HTTP_200_OK,
)
def update_syllabus(
    syllabus_id: UUID,
    request_data: SyllabusUpdateRequest,
    _: AuthenticatedUserDep,
    syllabus_service: SyllabusServiceDep,
    db_session: DBSessionDep,
):
    """Update a syllabus."""
    syllabus = syllabus_service.update_syllabus(db_session, syllabus_id, request_data)

    return SyllabusUpdateResponse(syllabus=syllabus)


@router.delete(
    "/{syllabus_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_syllabus(
    syllabus_id: UUID,
    _: AuthenticatedUserDep,
    syllabus_service: SyllabusServiceDep,
    db_session: DBSessionDep,
):
    """Delete a syllabus."""
    syllabus_service.delete_syllabus(db_session, syllabus_id)
