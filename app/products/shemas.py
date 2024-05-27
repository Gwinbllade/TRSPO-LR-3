from typing import Optional

from pydantic import BaseModel


class SProduct(BaseModel):
    id: int
    name: str
    cost: float
    category_id: int

    class Config:
        orm_mode = True


class SProductFilter(BaseModel):
    category_id: Optional[int]
    min_price: Optional[float] = None
    max_price: Optional[float] = None


class SUpdateProduct(BaseModel):
    id: int
    name: Optional[str] = None
    cost: Optional[float] = None
    category_id: Optional[int] = None


class SAddProduct(BaseModel):
    name: str
    cost: int
    category_id: int
