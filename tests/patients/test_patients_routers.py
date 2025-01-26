""""Module with API-tests of patients"""

from datetime import date, timedelta, datetime, timezone
from typing import Any

import pytest
from freezegun import freeze_time
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth import create_access_token
from auth.models import User
from patients.models import Patient, Diagnosis

@pytest.fixture(scope='function')
async def patients(db: AsyncSession) -> list[Patient]:
    """Fixture of getting test patients with diagnoses"""
    diagnoses: list[Diagnosis] = [
        Diagnosis(name=i_name)
        for i_name in ['cold', 'flu', 'asthma']
    ]
    patients: list[Patient] = [
        Patient(date_of_birth=i_date)
        for i_date in [date(1995, 1, 5), date(2005, 6, 7)]
    ]
    patients[0].diagnoses.extend([diagnoses[0], diagnoses[2]])
    patients[1].diagnoses.extend([diagnoses[1], diagnoses[2]])
    db.add_all(patients)
    await db.commit()
    return patients


class TestPatientsAPI:
    """Class with tests of operations with patients."""

    async def test_get_all_patients_success(
            self,
            client: AsyncClient,
            test_user_doctor: dict[str, Any],
            patients: list[Patient],
    ):
        """Test get all patietns success"""
        doctor: User = test_user_doctor.get('user')
        token_data: dict[str, str] = {'sub': str(doctor.id)}
        doctor_token: str = create_access_token(data=token_data)
        headers: dict[str, str] = {'Authorization': 'Bearer ' + doctor_token}
        response: Response = await client.get(
            url='/patients',
            headers=headers,
        )

        assert response.status_code == 200
        response_data: list[dict] = response.json()
        assert response_data

        for index, patient in enumerate(response_data):
            assert patient.get('id') == patients[index].id
            assert patient.get('date_of_birth') == patients[index].date_of_birth.strftime('%Y-%m-%d')
            patient_diagnoses: list[str] = patient.get('diagnoses')
            assert patient_diagnoses
            expected_diagnoses: set[str] = {diagnosis.name for diagnosis in patients[index].diagnoses}
            assert set(patient_diagnoses) == expected_diagnoses

    async def test_get_all_patients_not_doctor(
            self,
            client: AsyncClient,
            test_user_not_doctor: dict[str, Any],
    ):
        """Test get all patietns by user without doctor role"""
        not_doctor: User = test_user_not_doctor.get('user')
        token_data: dict[str, str] = {'sub': str(not_doctor.id)}
        not_doctor_token: str = create_access_token(data=token_data)
        headers: dict[str, str] = {'Authorization': 'Bearer ' + not_doctor_token}
        response: Response = await client.get(
            url='/patients',
            headers=headers,
        )

        assert response.status_code == 403
        assert 'detail' in response.json()
        assert response.json().get('detail') == 'Forbidden!'

    async def test_get_all_patients_user_not_found(
            self,
            client: AsyncClient,
    ):
        """Test get all patietns by user not existing in DB"""
        user_id: int = 100
        token_data: dict[str, str] = {'sub': str(user_id)}
        token: str = create_access_token(data=token_data)
        headers: dict[str, str] = {'Authorization': 'Bearer ' + token}
        response: Response = await client.get(
            url='/patients',
            headers=headers,
        )

        assert response.status_code == 401
        assert 'detail' in response.json()
        assert response.json().get('detail') == 'User is not found!'

    async def test_get_all_patients_user_id_invalid(
            self,
            client: AsyncClient,
    ):
        """Test get all patietns by user with token with no integer id"""
        token_data: dict[str, str] = {'sub': 'some_id'}
        token: str = create_access_token(data=token_data)
        headers: dict[str, str] = {'Authorization': 'Bearer ' + token}
        response: Response = await client.get(
            url='/patients',
            headers=headers,
        )

        assert response.status_code == 401
        assert 'detail' in response.json()
        assert response.json().get('detail') == 'User ID is invalid!'

    async def test_get_all_patients_user_id_not_found(
            self,
            client: AsyncClient,
    ):
        """Test get all patietns by user with token without 'sub' data"""
        token_data: dict[str, str] = {'not_sub': 'not_id'}
        token: str = create_access_token(data=token_data)
        headers: dict[str, str] = {'Authorization': 'Bearer ' + token}
        response: Response = await client.get(
            url='/patients',
            headers=headers,
        )

        assert response.status_code == 401
        assert 'detail' in response.json()
        assert response.json().get('detail') == 'User ID is not found!'


    async def test_get_all_patients_token_expired(
            self,
            client: AsyncClient,
            test_user_doctor: dict[str, Any],
    ):
        """Test get all patietns by doctor with expired token"""
        doctor: User = test_user_doctor.get('user')
        token_data: dict[str, str] = {'sub': str(doctor.id)}
        token: str = create_access_token(data=token_data, expires_delta=timedelta(days=30))
        headers: dict[str, str] = {'Authorization': 'Bearer ' + token}

        with freeze_time(datetime.now(timezone.utc) + timedelta(days=35)):
            response: Response = await client.get(
                url='/patients',
                headers=headers,
            )

        assert response.status_code == 401
        assert 'detail' in response.json()
        assert response.json().get('detail') == 'Token is expired!'

    async def test_get_all_patients_token_invalid(
            self,
            client: AsyncClient,
    ):
        """Test get all patietns by user with invalid token"""
        token: str = 'invalid_token'
        headers: dict[str, str] = {'Authorization': 'Bearer ' + token}
        response: Response = await client.get(
            url='/patients',
            headers=headers,
        )

        assert response.status_code == 401
        assert 'detail' in response.json()
        assert response.json().get('detail') == 'Token is invalid!'

    async def test_get_all_patients_invalid_header(
            self,
            client: AsyncClient,
    ):
        """Test get all patietns by user with invalid header"""
        headers: dict[str, str] = {'Authorization': 'Biarer token'}
        response: Response = await client.get(
            url='/patients',
            headers=headers,
        )
        assert response.status_code == 401
        assert 'detail' in response.json()
        assert response.json().get('detail') == 'Invalid Authorization header!'
    
    async def test_get_all_patients_missing_header(
            self,
            client: AsyncClient,
    ):
        """Test get all patietns by user request without auth header"""
        response: Response = await client.get(
            url='/patients',
        )
        assert response.status_code == 401
        assert 'detail' in response.json()
        assert response.json().get('detail') == 'Missing Authorization header!'
