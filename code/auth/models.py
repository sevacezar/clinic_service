"""Module with ORM model of users"""

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    """User ORM model."""
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password_hashed: Mapped[str]
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'), nullable=True)

    role = relationship('Role', back_populates='users')

    def __repr__(self) -> str:
        return f'<User {self.username}>'
    

class Role(Base):
    """Role ORM model."""
    __tablename__ = 'roles'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    users = relationship('User', back_populates='role')

    def __repr__(self) -> str:
        return f'<Role {self.name}>'
