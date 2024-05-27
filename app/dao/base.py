from app.database import async_session_maker
from sqlalchemy import select, insert, delete, update


class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            try:
                new_obj = cls.model(**data) 
                session.add(new_obj)  
                await session.commit()  
                await session.refresh(new_obj)  
                return new_obj  
            except Exception as e:
                await session.rollback()  
                raise e  
            

    @classmethod
    async def delete(cls, **filter_by):
        async with async_session_maker() as session:
            try:
                query = select(cls.model).filter_by(**filter_by)
                result = await session.stream(query)
                async for obj in result.scalars():
                    await session.delete(obj)
                await session.commit()
                return obj
            except Exception as e:
                await session.rollback()
                raise e

    @classmethod
    async def update(cls, filter_by, **data):
        async with async_session_maker() as session:
            try:
                query = await session.stream(
                    select(cls.model).filter_by(**filter_by)
                )
            
                async for obj in query.scalars():
                    for key, value in data.items():
                        setattr(obj, key, value)
                await session.commit()
                return obj
            except Exception as e:
                await session.rollback()
                raise e
