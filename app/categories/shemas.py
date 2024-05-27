from pydantic import BaseModel


class SCategory(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class SAddCategory(BaseModel):
    name: str


class SUpdateCategories(BaseModel):
    id: int
    name: str
