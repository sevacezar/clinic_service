"""Module with Pydantic-schemas of patients"""

from datetime import date, datetime

from pydantic import BaseModel


class DiagnosisPydanticOut(BaseModel):
    name: str


class PatientPydanticOut(BaseModel):
    id: int
    date_of_birth: date
    diagnoses: list[DiagnosisPydanticOut] = []
    created_at: datetime

    class Config:
        orm_mode = True


class PatientsPydanticOut(BaseModel):
    patients: list[PatientPydanticOut] = []
