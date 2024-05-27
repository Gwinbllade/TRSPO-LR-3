from fastapi import FastAPI

from app.users.router import router as router_users
from app.products.router import router as router_products
from app.categories.router import router as router_categories
from app.orders.router import router as router_orders
from fastapi_versioning import VersionedFastAPI

app = FastAPI()
app.include_router(router_users)
app.include_router(router_products)
app.include_router(router_categories)
app.include_router(router_orders)

app = VersionedFastAPI(app,
                       version_format='{major}',
                       prefix_format='/api/v{major}',
                       )
