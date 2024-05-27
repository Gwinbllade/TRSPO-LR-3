import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("username,email,password, status_code", [
    ("name", "name@gmail.com", "text", 200),
    ("name", "name@gmail.com", "text", 500),
    ("name", "xxxx", "psss", 422)
])
async def test_register(username, email, password, status_code, ac: AsyncClient):
    response = await ac.post("/api/v2/users/auth/register", params={
        "username": username,
        "email": email,
        "password": password
    })
    assert response.status_code == status_code


@pytest.mark.parametrize("email, password, status_code", [
    ("bobsmith@gmail.com", "hashedpassword3", 200),
    ("bobsmith@gmail.com", "hashedpassword2", 401),
    ("test@gmail.com", "hashedpassword3", 401),
    ("janedoe@gmail.com", "hashedpassword2", 200)

])
async def test_login(email, password, status_code, ac: AsyncClient):
    response = await ac.post("/api/v2/users/auth/login", params={
        "email": email,
        "password": password
    })
    assert response.status_code == status_code


@pytest.mark.parametrize("is_admin", [
    True,
    False
])
async def test_get_users(is_admin, authenticated_ac_admin: AsyncClient, authenticated_ac_buyer: AsyncClient):
    if is_admin:
        response = await authenticated_ac_admin.get("/api/v2/users")
        assert response.status_code == 200
    else:
        response = await authenticated_ac_buyer.get("/api/v2/users")
        assert response.status_code == 403


@pytest.mark.parametrize("is_auth", [
    True,
    False
])
async def test_update_user(is_auth, ac: AsyncClient, authenticated_ac_buyer: AsyncClient):
    if is_auth:
        response = await authenticated_ac_buyer.patch("/api/v2/users",
                                                      params={"username": "TestUser", "password": "New"})
        assert response.status_code == 200
    else:
        response = await ac.patch("/api/v2/users", params={"username": "TestUser", "password": "New"})
        assert response.status_code == 401


@pytest.mark.parametrize("is_admin, user_id, status_code", [
    (True, 2, 200),
    (True, 2000, 404),
    (False, 1, 403)
])
async def test_get_user_by_id(is_admin: bool, user_id: int, status_code: int,
                              authenticated_ac_admin: AsyncClient, authenticated_ac_buyer: AsyncClient):
    ac = authenticated_ac_admin if is_admin else authenticated_ac_buyer
    url = f"/api/v2/users/{user_id}"
    response = await ac.get(url)
    print(response.status_code)
    assert response.status_code == status_code


@pytest.mark.parametrize("is_auth, status_code", [
    (True, 200),
    (False, 401)
])
async def test_user_logout(is_auth: bool, authenticated_ac_buyer: AsyncClient, ac: AsyncClient, status_code: int):
    user = authenticated_ac_buyer if is_auth else ac
    url = f"/api/v2/users/auth/logout"
    response = await user.post(url)
    assert response.status_code == status_code
