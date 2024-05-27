from typing import List

from fastapi import APIRouter, HTTPException, Depends, status

from fastapi_versioning import version
from app.orders.dao import OrderDAO
from app.orders.shemas import SOrder, SOrderCrate, SOrderUpdate
from app.orders.models import OrderStatus
from app.products.dao import ProductDAO
from app.users.dependencies import get_current_user
from app.users.models import User, UserRole

router = APIRouter(
    prefix="/orders",
    tags=['Orders']
)


@router.get("")
async def get_orders(current_user: User = Depends(get_current_user)) -> List[SOrder]:
    if current_user.role == UserRole.ADMIN:
        return await OrderDAO.find_all()
    else:
        return await OrderDAO.find_all(user_id=current_user.id)


@router.get("/{status}")
@version(2)
async def get_orders_by_status(status: OrderStatus, current_user: User = Depends(get_current_user)) -> List[SOrder]:
    if current_user.role == UserRole.ADMIN:
        return await OrderDAO.find_all(status=status)
    else:
        raise HTTPException(403)


@router.post("")
async def create_order(data: SOrderCrate = Depends(), current_user: User = Depends(get_current_user)) -> SOrder:
    try:
        new_order = await OrderDAO.create(user_id=current_user.id, product_id=data.product_id)
        return new_order
    except:
        raise HTTPException(501, detail="Order not create. Check the parameters ")


@router.delete("/{order_id}")
async def delete(order_id: int, current_user: User = Depends(get_current_user)) -> SOrder:
    if current_user.role == UserRole.ADMIN:
        try:
            result = await OrderDAO.delete(id=order_id)
            return result
        except:
            raise HTTPException(501, detail="Order not delete. Check the product id ")
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


@router.patch("/status/{order_id}")
async def update_status(order_id:int, order_data: SOrderUpdate = Depends(), current_user: User = Depends(get_current_user)) -> SOrder:
    if current_user.role == UserRole.ADMIN:
        product = await OrderDAO.find_by_id(order_id)
        if not product:
            raise HTTPException(status_code=404, detail="Order not found")
        update_data = order_data.dict(exclude_none=True)
        try:
            updated_prodcut = await OrderDAO.update(filter_by={"id": order_id}, **update_data)
            return updated_prodcut
        except:
            raise HTTPException(500, detail="Failed to update order status ")
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
