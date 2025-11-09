# routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.ext.asyncio import AsyncSession
import models, schemas, crud
from database import get_db
from auth_utils import get_current_user

router = APIRouter(tags=["Users"], prefix="/users")

# -------------------- GET CURRENT USER --------------------
@router.get("/me", response_model=schemas.UserOut)
async def get_me(current_user: models.User = Depends(get_current_user)):
    return current_user

# -------------------- UPDATE CURRENT USER --------------------
@router.put("/me", response_model=schemas.UserOut)
async def update_me(
    username: str | None = Form(None),
    email: str | None = Form(None),
    password: str | None = Form(None),
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    update_data = schemas.UserUpdate(
        username=username,
        email=email,
        password=password
    )
    updated_user = await crud.update_user(db, current_user.id, update_data)
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Update failed")
    return updated_user

# -------------------- DELETE CURRENT USER --------------------
@router.delete("/me", response_model=schemas.UserOut)
async def delete_me(
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    deleted_user = await crud.delete_user(db, current_user.id)
    if not deleted_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Delete failed")
    return deleted_user
