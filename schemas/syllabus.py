from datetime import date
from typing import List
from pydantic import BaseModel

from custom_types.enums import SubjectCode, SyllabusLevel

from models import Syllabus


class SyllabusCreateRequest(BaseModel):
    name: str
    description: str
    code: SubjectCode
    level: SyllabusLevel
    examination_date: date


class SyllabusCreateResponse(BaseModel):
    syllabus: Syllabus


class SyllabusGetResponse(BaseModel):
    syllabus: Syllabus


class SyllabusesGetResponse(BaseModel):
    syllabuses: List[Syllabus]


class SyllabusUpdateRequest(BaseModel):
    name: str | None = None
    description: str | None = None
    code: SubjectCode | None = None
    level: SyllabusLevel | None = None
    examination_date: date | None = None


class SyllabusUpdateResponse(BaseModel):
    syllabus: Syllabus
