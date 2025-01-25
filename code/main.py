"""Main module. API launch point."""

from fastapi import FastAPI

from patients.router import router as patients_router


app: FastAPI = FastAPI(
    description='This is clinic service API',
    title='Clinic service API',
)

app.include_router(patients_router)
