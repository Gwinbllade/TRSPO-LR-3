from datetime import date

from sqlalchemy import select, insert, delete, update

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.orders.models import Order, OrderStatus


class OrderDAO(BaseDAO):
    model = Order

    @classmethod
    async def create(cls, **data):
        user_id = data.pop('user_id')
        product_id = data.pop('product_id')
        async with async_session_maker() as session:
            try:
                new_order = cls.model(user_id=user_id, product_id=product_id, date=date.today(), status=OrderStatus.PROCESSING, **data)
                session.add(new_order)
                await session.commit()
                await session.refresh(new_order)
                return new_order
            except Exception as e:
                await session.rollback()
                raise e