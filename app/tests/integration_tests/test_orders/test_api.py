import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("is_admin, status_code", [
    (True, 200),
    (False, 200),
])
async def test_get_orders(authenticated_ac_buyer: AsyncClient, authenticated_ac_admin: AsyncClient, is_admin: bool,
                          status_code: int):
    user = authenticated_ac_admin if is_admin else authenticated_ac_buyer
    url = f"api/v2/orders"
    response = await user.get(url)
    assert response.status_code == status_code


@pytest.mark.parametrize("order_id, is_admin, status_code", [
    (1, True, 200),
    (2000, True, 501),
    (1, False, 403),
])
async def test_order_delete(status_code, authenticated_ac_buyer: AsyncClient,
                            authenticated_ac_admin: AsyncClient, is_admin, order_id: int
                            ):
    user = authenticated_ac_admin if is_admin else authenticated_ac_buyer
    response = await user.delete(f"api/v2/orders/{order_id}")
    assert response.status_code == status_code


@pytest.mark.parametrize("product_id, is_auth, status_code", [
    (1, True, 200),
    (1, False, 401),
    (200, True, 501),
])
async def test_order_create(status_code, authenticated_ac_buyer: AsyncClient,
                            ac: AsyncClient, is_auth
                            , product_id: int):
    user = authenticated_ac_buyer if is_auth else ac
    response = await user.post("api/v2/orders", params={
        "product_id": product_id,
    })
    assert response.status_code == status_code


@pytest.mark.parametrize("is_admin,order_status, status_code", [
    (True, "In processing", 200),
    (True, "Shipped", 200),
    (True, "Delivered", 200),
    (False, "Delivered", 403),
])
async def test_get_orders_by_status(authenticated_ac_buyer: AsyncClient, authenticated_ac_admin: AsyncClient,
                                    is_admin: bool,
                                    status_code: int, order_status: str):
    user = authenticated_ac_admin if is_admin else authenticated_ac_buyer
    url = f"/api/v2/orders/{order_status}"
    response = await user.get(url)
    assert response.status_code == status_code


@pytest.mark.parametrize("order_id ,is_admin, order_status, status_code", [
    (3, True, "Shipped", 200),
    (1, True, "Shipped", 404),
    (1, False, "In processing", 403),

])
async def test_order_status_update(status_code, order_id, authenticated_ac_buyer: AsyncClient,
                                   authenticated_ac_admin: AsyncClient, is_admin, order_status
                                   ):
    user = authenticated_ac_admin if is_admin else authenticated_ac_buyer
    response = await user.patch(f"api/v2/orders/status/{order_id}", params={
        "id": order_id,
        "status": order_status
    })

    assert response.status_code == status_code
