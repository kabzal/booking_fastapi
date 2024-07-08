from datetime import datetime

from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

import config
from . import models, schemas

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")


async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(models.User).where(models.User.username == username))
    user = result.scalars().first()
    if user:
        return user
    else:
        return False


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(models.User).where(models.User.email == email))
    user = result.scalars().first()
    if user:
        return user
    else:
        return False


async def create_user(db: AsyncSession, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)

    if user.username == config.ADMIN_NAME and user.email == config.ADMIN_EMAIL and user.password == config.ADMIN_PASS:
        is_admin = True
    else:
        is_admin = False

    db_user = models.User(username=user.username,
                          email=user.email,
                          hashed_password=hashed_password,
                          is_admin=is_admin)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_tables(db: AsyncSession):
    result = await db.execute(select(models.Table))
    tables = result.scalars().all()
    return tables


async def get_available_table(
        db: AsyncSession,
        table_type: schemas.TableType,
        start_time: datetime,
        end_time: datetime
):
    start_time = start_time.replace(tzinfo=None)
    end_time = end_time.replace(tzinfo=None)
    result = await db.execute(
        select(models.Table).where(
            models.Table.table_type == table_type,
            ~models.Table.bookings.any(
                and_(
                    models.Booking.start_time < end_time,
                    models.Booking.end_time > start_time
                )
            )
        )
    )
    table = result.scalars().first()
    return table


async def create_table(db: AsyncSession, table: schemas.TableCreate):
    db_table = models.Table(**table.dict())
    db.add(db_table)
    await db.commit()
    await db.refresh(db_table)
    return db_table


async def delete_table(db: AsyncSession, table_id: int):
    table_query = await db.execute(
        select(models.Table).where(
            models.Table.id == table_id
        )
    )
    table_chosen = table_query.scalars().first()

    if not table_chosen:
        raise HTTPException(status_code=404, detail="Table not found")

    await db.delete(table_chosen)
    await db.commit()
    return {"message": f"Table №{table_id} deleted successfully"}


async def create_booking(db: AsyncSession, booking: schemas.BookingCreate):
    # Преобразование datetime к offset-naive
    start_time_naive = booking.start_time.replace(tzinfo=None)
    end_time_naive = booking.end_time.replace(tzinfo=None)

    db_booking = models.Booking(
        start_time=start_time_naive,
        end_time=end_time_naive,
        user_id=booking.user_id,
        table_id=booking.table_id
    )
    db.add(db_booking)
    await db.commit()
    await db.refresh(db_booking)
    return db_booking


async def get_bookings(db: AsyncSession, current_user: schemas.User):
    result = await db.execute(
        select(models.Booking).where(
            models.Booking.user_id == current_user.id
        )
    )
    bookings = result.scalars().all()
    return bookings


async def get_upcoming_bookings(db: AsyncSession, current_user: schemas.User):
    result = await db.execute(
        select(models.Booking).where(
            models.Booking.end_time > datetime.now().replace(tzinfo=None),
            models.Booking.user_id == current_user.id
        )
    )
    upcoming_bookings = result.scalars().all()
    return upcoming_bookings


async def get_previous_bookings(db: AsyncSession, current_user: schemas.User):
    result = await db.execute(
        select(models.Booking).where(
            models.Booking.end_time <= datetime.now().replace(tzinfo=None),
            models.Booking.user_id == current_user.id
        )
    )
    previous_bookings = result.scalars().all()
    return previous_bookings


async def admin_get_all_bookings(db: AsyncSession):
    result = await db.execute(select(models.Booking))
    bookings = result.scalars().all()
    return bookings


async def delete_booking(
        db: AsyncSession,
        booking_id: int,
        current_user: schemas.User
):
    booking_query = await db.execute(
        select(models.Booking).where(
            models.Booking.id == booking_id
        )
    )
    booking_chosen = booking_query.scalars().first()

    if not booking_chosen:
        raise HTTPException(status_code=404, detail="Booking not found")

    if not (current_user.is_admin or current_user.id == booking_chosen.user_id):
        raise HTTPException(status_code=403, detail="Access denied: only Admin or "
                                                    "booking creator can delete this booking")

    if not current_user.is_admin and booking_chosen.start_time <= datetime.now().replace(tzinfo=None):
        raise HTTPException(status_code=403, detail="Access denied: as a booking creator, "
                                                    "you can delete only upcoming bookings")

    await db.delete(booking_chosen)
    await db.commit()
    return {"message": f"Booking №{booking_id} deleted successfully"}


