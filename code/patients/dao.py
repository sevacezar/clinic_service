"""Module with data access object of Patient"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .models import Patient

class PatientsDAO:
    async def get_all(
            session: AsyncSession,
            offset: int = 0,
            limit: int | None = None
        ) -> list[Patient]:
        """Get all patients"""
        query = select(Patient).options(selectinload(Patient.diagnoses))
        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)

        res = await session.execute(query)
        patients: list[Patient] = res.scalars().all()

        return patients
