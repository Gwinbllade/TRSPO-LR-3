import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("is_auth, status_code, is_product_id, category_id", [
    (True, 200, False, 0),
    (False, 200, False, 0),
    (True, 200, True, 1),
    (True, 200, True, -1)
])
async def test_get_products(authenticated_ac_buyer: AsyncClient, ac: AsyncClient, is_auth: bool, status_code: int,
                            is_product_id: int, category_id: str):
    user = authenticated_ac_buyer if is_auth else ac
    url = f"api/v2/products?category_id={category_id}" if is_product_id else f"api/v2/products"
    response = await user.get(url)
    assert response.status_code == status_code

@pytest.mark.parametrize("name, cost, category_id, is_admin, status_code", [
    ("test", 200, 1, True, 200),
    ("test", 200, 999, True, 501),
    ("test", 200, 1, False, 403),
])
async def test_product_add(name, cost, category_id, status_code, authenticated_ac_buyer: AsyncClient,
                           authenticated_ac_admin: AsyncClient, is_admin
                           ):
    user = authenticated_ac_admin if is_admin else authenticated_ac_buyer
    response = await user.post("api/v2/products", params={
        "name": name,
        "cost": cost,
        "category_id": category_id
    })
    assert response.status_code == status_code

@pytest.mark.parametrize("id, name, cost, category_id, is_admin, status_code", [
    (1, "newtest", 200, 1, True, 200),
    (2000, "test", 200, 999, True, 404),
    (1, "test", 200, 1, False, 403),
])
async def test_product_update(name, cost, category_id, status_code, authenticated_ac_buyer: AsyncClient,
                              authenticated_ac_admin: AsyncClient, is_admin, id: int
                              ):
    user = authenticated_ac_admin if is_admin else authenticated_ac_buyer
    response = await user.patch("api/v2/products", params={
        "id": id,
        "name": name,
        "cost": cost,
        "category_id": category_id
    })
    assert response.status_code == status_code


@pytest.mark.parametrize("id, is_admin, status_code", [
    (1, True, 200),
    (2000, True, 501),
    (1, False, 403),
])
async def test_product_delete(status_code, authenticated_ac_buyer: AsyncClient,
                              authenticated_ac_admin: AsyncClient, is_admin, id: int
                              ):
    user = authenticated_ac_admin if is_admin else authenticated_ac_buyer
    response = await user.delete(f"api/v2/products/{id}")
    assert response.status_code == status_code
