"""Module with ORM models of patiens, diagnoses"""

from datetime import date, datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base

class Patient(Base):
    __tablename__ = 'patients'

    id: Mapped[int] = mapped_column(primary_key=True)
    date_of_birth: Mapped[date]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    

