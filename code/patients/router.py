"""Module with fastapi views of patients functionality"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth.dependencies import get_current_doctor_user
from auth.models import User
from dependencies import get_session
from patients.dao import PatientsDAO
from patients.models import Patient
from patients.schemas import PatientPydanticOut


router: APIRouter = APIRouter(prefix='/patients', tags=['Patients'])


@router.get('', response_model=list[PatientPydanticOut])
async def get_all_patients(
    doctor: User = Depends(get_current_doctor_user),
    session: AsyncSession = Depends(get_session),
):
    """Get all patients from DB"""
    patients: list[Patient] = await PatientsDAO.get_all(session=session)
    patients_dicts: list[dict] = [patient.to_dict() for patient in patients]
    return patients_dicts
    