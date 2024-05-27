import json

import asyncio
from datetime import datetime

import pytest
from sqlalchemy import insert
from app.config import settings
from app.database import Base, async_session_maker, engine
from app.users.auth import get_password_hash
from app.users.models import User
from app.categories.models import Category
from app.products.models import Product
from app.orders.models import Order

from fastapi.testclient import TestClient
from httpx import AsyncClient
from app.main import app as fastapi_app


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"app/tests/mock_{model}.json", "r") as file:
            return json.load(file)

    users = open_mock_json("users")
    categories = open_mock_json("categories")
    products = open_mock_json("products")
    orders = open_mock_json("orders")

    for order in orders:
        order["date"] = datetime.strptime(order["date"], "%Y-%m-%d")

    for user in users:
        user["hashed_password"] = get_password_hash(user["hashed_password"])

    async with async_session_maker() as session:
        add_users = insert(User).values(users)
        add_categories = insert(Category).values(categories)
        add_products = insert(Product).values(products)
        add_orders = insert(Order).values(orders)

        await session.execute(add_users)
        await session.execute(add_categories)
        await session.execute(add_products)
        await session.execute(add_orders)

        await session.commit()


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def authenticated_ac_buyer():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        await ac.post("/api/v2/users/auth/login", params={
            "email": "janedoe@gmail.com",
            "password": "hashedpassword2",
        })
        assert ac.cookies["access_token"]
        yield ac


@pytest.fixture(scope="session")
async def authenticated_ac_admin():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        await ac.post("/api/v2/users/auth/login", params={
            "email": "johndoe@gmail.com",
            "password": "hashedpassword1",
        })
        assert ac.cookies["access_token"]
        yield ac




