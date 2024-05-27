from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.database import Base


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    products = relationship("Product", backref="category", cascade="all, delete, delete-orphan")
