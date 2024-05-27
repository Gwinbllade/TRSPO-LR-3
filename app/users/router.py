from typing import List

from fastapi import APIRouter, HTTPException, Depends, Response, status, Request

from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.dao import UserDAO
from app.users.dependencies import get_current_user
from app.users.models import User, UserRole
from app.users.shemas import SUser, SUserAuth, SUserUpdate, SUserLogin, SUserInfo

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.get("")
async def get_users(current_user: User = Depends(get_current_user)) -> List[SUser]:
    if current_user.role == UserRole.ADMIN:
        users = await UserDAO.find_all()
        return users
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

@router.get("/me")
async def get_user_info(current_user: User = Depends(get_current_user)) -> SUserInfo:
    user = await UserDAO.find_one_or_none(id=current_user.id)
    return SUserInfo.from_orm(user)

@router.get("/{user_id}")
async def get_user(user_id: int, current_user: User = Depends(get_current_user)) -> SUser:
    if current_user.role == UserRole.ADMIN:
        user = await UserDAO.find_one_or_none(id=user_id)
        if user:
            return user
        else:
            raise HTTPException(status_code=404, detail="User not found")
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


@router.post("/auth/register")
async def register(user_data: SUserAuth = Depends()) -> str:
    existing_user = await UserDAO.find_all(email=user_data.email)
    if existing_user:
        raise HTTPException(status_code=500)
    else:
        print(user_data.password, user_data.email)
        hashed_password = get_password_hash(user_data.password)
        await UserDAO.add(email=user_data.email,
                          hashed_password=hashed_password,
                          username=user_data.username,
                          role="buyer")

        return "User created successfully"


@router.patch("")
async def update(user_data: SUserUpdate = Depends(), current_user: User = Depends(get_current_user)) -> SUserInfo:
    update_data = user_data.dict(exclude_none=True)
    if update_data.get("password"):
        update_data["hashed_password"] = update_data.pop("password")
    updata_user = await UserDAO.update(filter_by={"id": current_user.id}, **update_data)

    if updata_user is not None:
        return SUserInfo.from_orm(updata_user)
    else:
        raise HTTPException(status_code=500, detail="Failed to update user")


@router.post("/auth/login")
async def login_user(response: Response, user_date: SUserLogin = Depends()):
    user = await authenticate_user(user_date.email, user_date.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("access_token", access_token, httponly=True)
    return "Successfully login"


@router.post("/auth/logout")
async def logout(request: Request, response: Response):
    if "access_token" in request.cookies:
        response.delete_cookie("access_token")
        return {"message": "User logout"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
