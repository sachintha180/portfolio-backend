from enum import Enum


class UserType(str, Enum):
    STUDENT = "student"
    ADMIN = "admin"


class SubjectCode(str, Enum):
    EDEXCEL_IGCSE_CS = "4CP0"
    EDEXCEL_IGCSE_ICT = "41T1"
    EDEXCEL_IAL_IT = "X/YIT11"
    CAMBRIDGE_OLEVEL_CS = "2210"
    CAMBRIDGE_IAL_CS = "9618"
    IB_DIPLOMA_CS = "HL, 2014"


class SyllabusLevel(str, Enum):
    IGCSE = "igcse"
    OLEVEL = "olevel"
    ALEVEL = "alevel"
    DIPLOMA = "diploma"


class FileType(str, Enum):
    NOTE = "note"
    VIDEO = "video"
    CODE = "code"
    EXERCISE = "exercise"
    TEST = "test"
