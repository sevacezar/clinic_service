"""Module with ORM model of users"""

from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class User(Base):
    """User ORM model."""
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password_hashed: Mapped[str]
    is_doctor: Mapped[bool] = mapped_column(default=False)

    def __repr__(self) -> str:
        return f'<User {self.username}>'


