from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi_versioning import version

from app.categories.dao import CategoriaDAO
from app.categories.shemas import SCategory, SAddCategory, SUpdateCategories
from app.users.dependencies import get_current_user
from app.users.models import User, UserRole

router = APIRouter(
    prefix="/categories",
    tags=['Categories']
)


@router.get("")
async def get_categories() -> List[SCategory]:
    categories = await CategoriaDAO.find_all()
    return categories


@router.get("/{category_id}")
@version(2)
async def get_category(category_id: int) -> SCategory:
    categories = await CategoriaDAO.find_one_or_none(id=category_id)
    if categories is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return categories


@router.post("")
async def add(args: SAddCategory = Depends(), current_user: User = Depends(get_current_user)) -> SCategory:
    if current_user.role == UserRole.ADMIN:
        try:
            new_categories = await CategoriaDAO.add(name=args.name)
            return new_categories
        except:
            raise HTTPException(501, detail="Category not added. Check the parameters ")
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


@router.delete("/{category_id}")
async def delete(category_id: int, current_user: User = Depends(get_current_user)) -> SCategory:
    if current_user.role == UserRole.ADMIN:
        try:
            result = await CategoriaDAO.delete(id=category_id)
            return result
        except:
            raise HTTPException(501, detail="Category not delete. Check the product id ")
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


@router.put("")
async def update(category_data: SUpdateCategories = Depends(),
                 current_user: User = Depends(get_current_user)) -> SCategory:
    if current_user.role == UserRole.ADMIN:
        category = await CategoriaDAO.find_by_id(category_data.id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        update_data = category_data.dict(exclude_none=True)
        try:
            updated_count = await CategoriaDAO.update(filter_by={"id": category_data.id}, **update_data)
            return updated_count
        except:
            raise HTTPException(status_code=500, detail="Failed to update category")
