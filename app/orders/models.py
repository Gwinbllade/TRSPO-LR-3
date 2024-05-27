from sqlalchemy import Column, Integer, String, ForeignKey, Date, Enum as PgEnum

from enum import Enum

from app.database import Base


class OrderStatus(str, Enum):
    PROCESSING = "In processing"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"))
    date = Column(Date, nullable=False)
    status = Column(PgEnum(OrderStatus, length=15), nullable=False)
    product_id = Column(ForeignKey("products.id", ondelete="CASCADE"))
