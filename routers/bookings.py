from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth import get_current_active_user
from models import schemas, crud
from models.database import get_db

router = APIRouter(
    prefix="/bookings",
    tags=["bookings"],
)


@router.post("/create", response_model=schemas.BookingShow)
async def create_booking(
        current_user: Annotated[schemas.User, Depends(get_current_active_user)],
        start_time: datetime = Query(..., description="Start time of the booking"),
        end_time: datetime = Query(..., description="End time of the booking"),
        table_type: schemas.TableType = Query(..., description="Type of the table"),
        db: AsyncSession = Depends(get_db)):

    # Проверка, что end_time позже start_time
    if end_time <= start_time:
        raise HTTPException(status_code=400, detail="End time must be after start time")

    # Проверка, что разница между start_time и end_time не менее 1 часа и не более 4 часов
    duration = end_time - start_time
    if duration < timedelta(hours=1) or duration > timedelta(hours=4):
        raise HTTPException(status_code=400, detail="Booking duration must be between 1 and 4 hours")

    # Поиск доступного стола указанного типа
    table = await crud.get_available_table(db, table_type, start_time, end_time)
    if not table:
        raise HTTPException(status_code=404, detail="No available table of the selected type")

    # Создание объекта бронирования
    booking_data = schemas.BookingCreate(
        start_time=start_time,
        end_time=end_time,
        user_id=current_user.id,
        table_id=table.id,
        table_type=table_type,
    )
    new_booking = await crud.create_booking(db=db, booking=booking_data)
    return new_booking


@router.get("/my_bookings", response_model=list[schemas.BookingShow])
async def read_bookings(
        current_user: Annotated[schemas.User, Depends(get_current_active_user)],
        db: AsyncSession = Depends(get_db)
):
    bookings = await crud.get_bookings(db=db, current_user=current_user)
    return bookings


@router.get("/my_upcoming_bookings", response_model=list[schemas.BookingShow])
async def read_upcoming_bookings(
        current_user: Annotated[schemas.User, Depends(get_current_active_user)],
        db: AsyncSession = Depends(get_db)
):
    bookings = await crud.get_upcoming_bookings(db=db, current_user=current_user)
    return bookings


@router.get("/my_previous_bookings", response_model=list[schemas.BookingShow])
async def read_previous_bookings(
        current_user: Annotated[schemas.User, Depends(get_current_active_user)],
        db: AsyncSession = Depends(get_db)
):
    bookings = await crud.get_previous_bookings(db=db, current_user=current_user)
    return bookings


@router.get("/get_all_bookings", response_model=list[schemas.BookingShow])
async def get_all_bookings(
        current_user: Annotated[schemas.User, Depends(get_current_active_user)],
        db: AsyncSession = Depends(get_db)
):
    """
    Available only for Admin: get all bookings made by all users
    """
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Access denied: only Admin can see all bookings")
    bookings = await crud.admin_get_all_bookings(db=db)
    return bookings


@router.delete("/delete_booking/{booking_id}")
async def delete_booking(
        current_user: Annotated[schemas.User, Depends(get_current_active_user)],
        booking_id: int,
        db: AsyncSession = Depends(get_db),
):
    """
        Users can delete their upcoming bookings. Admin can delete any bookings.
    """
    return await crud.delete_booking(db=db, booking_id=booking_id, current_user=current_user)
