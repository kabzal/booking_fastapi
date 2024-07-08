from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth import get_current_active_user
from models import schemas, crud
from models.database import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/register", response_model=schemas.User)
async def register(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.create_user(db=db, user=user)


@router.get("/me", response_model=schemas.User)
async def read_users_me(
        current_user: Annotated[schemas.User, Depends(get_current_active_user)]
):
    return current_user
