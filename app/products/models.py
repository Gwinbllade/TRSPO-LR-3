from sqlalchemy import Column, Integer, String, ForeignKey, Float
from app.database import Base


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    cost = Column(Float, nullable=False)
    category_id = Column(ForeignKey("categories.id", ondelete="CASCADE"))
