"""Module with Pydantic-schemas of patients"""

from datetime import date, datetime

from pydantic import BaseModel


class PatientPydanticOut(BaseModel):
    """Output Patient scheme"""
    id: int
    date_of_birth: date
    diagnoses: list[str] = []
    created_at: datetime

    class Config:
        orm_mode = True
