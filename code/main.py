"""Main module. API launch point."""

from fastapi import FastAPI

from auth.router import router as auth_router
from patients.router import router as patients_router


app: FastAPI = FastAPI(
    description='This is clinic service API',
    title='Clinic service API',
)

app.include_router(patients_router)
app.include_router(auth_router)
