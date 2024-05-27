import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("is_auth, status_code", [
    (True, 200),
    (False, 200),
])
async def test_get_categories(authenticated_ac_buyer: AsyncClient, ac: AsyncClient, is_auth: bool, status_code: int):
    user = authenticated_ac_buyer if is_auth else ac
    url = f"api/v2/categories"
    response = await user.get(url)
    assert response.status_code == status_code


@pytest.mark.parametrize("is_auth, status_code, category_id", [
    (True, 404, 0),
    (False, 404, 0),
    (True, 200, 1),
    (True, 404, -1)
])
async def test_get_categories_by_id(authenticated_ac_buyer: AsyncClient, ac: AsyncClient, is_auth: bool,
                                    status_code: int,
                                    category_id: str):
    user = authenticated_ac_buyer if is_auth else ac
    url = f"api/v2/categories/{category_id}"
    response = await user.get(url)
    assert response.status_code == status_code


@pytest.mark.parametrize("name, is_admin, status_code", [
    ("test", True, 200),
    ("test", False, 403),
])
async def test_category_add(name, status_code, authenticated_ac_buyer: AsyncClient,
                            authenticated_ac_admin: AsyncClient, is_admin
                            ):
    user = authenticated_ac_admin if is_admin else authenticated_ac_buyer
    response = await user.post("api/v2/categories", params={
        "name": name,
    })
    assert response.status_code == status_code


@pytest.mark.parametrize("id, name, is_admin, status_code", [
    (1, "newtest", False, 405),

])
async def test_category_update(name, status_code, id, authenticated_ac_buyer: AsyncClient,
                               authenticated_ac_admin: AsyncClient, is_admin
                               ):
    user = authenticated_ac_admin if is_admin else authenticated_ac_buyer
    response = await user.patch(f"api/v2/categories/{id}", params={
        "name": name
    })
    assert response.status_code == status_code


@pytest.mark.parametrize("id, is_admin, status_code", [
    (1, True, 200),
    (2000, True, 501),
    (1, False, 403),
])
async def test_category_delete(status_code, authenticated_ac_buyer: AsyncClient,
                               authenticated_ac_admin: AsyncClient, is_admin, id: int
                               ):
    user = authenticated_ac_admin if is_admin else authenticated_ac_buyer
    response = await user.delete(f"api/v2/categories/{id}")
    assert response.status_code == status_code
