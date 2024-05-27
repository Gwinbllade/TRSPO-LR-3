from sqlalchemy import Column, Integer, String, Enum as PgEnum
from enum import Enum
from app.database import Base


class UserRole(str, Enum):
    ADMIN = "admin"
    BUYER = "buyer"


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(120), nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    role = Column(PgEnum(UserRole), nullable=False)

