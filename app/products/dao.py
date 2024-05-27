from app.dao.base import BaseDAO
from app.products.models import Product


class ProductDAO(BaseDAO):
    model = Product
