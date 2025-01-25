"""Module with ORM models of patiens, diagnoses"""

from datetime import date, datetime
from typing import Any

from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


patient_diagnosis_association = Table(
    'patient_diagnosis',
    Base.metadata,
    Column(
        'patient_id',
        Integer,
        ForeignKey('patients.id', ondelete='CASCADE'), 
        primary_key=True,
    ),
    Column(
        'diagnosis_id',
        Integer,
        ForeignKey('diagnoses.id', ondelete='CASCADE'),
        primary_key=True
    ),
)


class Patient(Base):
    __tablename__ = 'patients'

    id: Mapped[int] = mapped_column(primary_key=True)
    date_of_birth: Mapped[date]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    diagnoses = relationship(
        'Diagnosis',
        secondary=patient_diagnosis_association,
        back_populates='patients'
    )

    def __repr__(self) -> str:
        return f'<Patient {self.id}>'
    
    def to_dict(self) -> dict:
        """Convert ORM model to dict"""
        patient_dict: dict[str, Any] = {
            'id': self.id,
            'date_of_birth': self.date_of_birth,
            'created_at': self.created_at,
        }
        diagnoses: list[str] = [diagnosis.name for diagnosis in self.diagnoses]
        patient_dict.update({'diagnoses': diagnoses})

        return patient_dict


class Diagnosis(Base):
    __tablename__ = 'diagnoses'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    patients = relationship(
        'Patient',
        secondary=patient_diagnosis_association,
        back_populates='diagnoses'
    )

    def __repr__(self) -> str:
        return f'<Diagnosis {self.name}>'
    


