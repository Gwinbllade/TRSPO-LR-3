from app.categories.models import Category
from app.dao.base import BaseDAO


class CategoriaDAO(BaseDAO):
    model = Category
