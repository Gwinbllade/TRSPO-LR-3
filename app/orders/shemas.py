from typing import List

from fastapi import Query
from pydantic import BaseModel
from datetime import date
from app.orders.models import OrderStatus

class SOrder(BaseModel):
    id: int
    user_id: int
    date: date
    status: str
    product_id: int

    class Config:
        orm_mode = True


class SOrderCrate(BaseModel):
    product_id: int


class SOrderUpdate(BaseModel):
    status: OrderStatus
