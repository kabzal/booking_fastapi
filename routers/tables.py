from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth import get_current_active_user
from models import schemas, crud
from models.database import get_db

router = APIRouter(
    prefix="/tables",
    tags=["tables"],
)


@router.post("/add_table", response_model=schemas.Table)
async def add_table(
        current_user: Annotated[schemas.User, Depends(get_current_active_user)],
        table: schemas.TableCreate = Depends(),
        db: AsyncSession = Depends(get_db),
):
    """
        Available only for Admin: add new tables to the database
    """
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Access denied: only Admin can add new tables")
    return await crud.create_table(db=db, table=table)


@router.get("/", response_model=list[schemas.Table])
async def read_tables(db: AsyncSession = Depends(get_db)):
    tables = await crud.get_tables(db=db)
    return tables


@router.delete("/delete_table/{table_id}")
async def delete_table(
        current_user: Annotated[schemas.User, Depends(get_current_active_user)],
        table_id: int,
        db: AsyncSession = Depends(get_db),
):
    """
        Available only for Admin: delete coffeeshop table from the database
    """
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Access denied: only Admin can delete tables")
    return await crud.delete_table(db=db, table_id=table_id)
