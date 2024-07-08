from datetime import datetime
from enum import Enum

from fastapi import HTTPException
from pydantic import BaseModel, field_validator


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_admin: bool
    disabled: bool

    class Config:
        orm_mode = True


class TableType(str, Enum):
    two_guest_table = "two guest table"
    four_guest_table = "four guest table"
    eight_guest_table = "eight guest table"


class TableBase(BaseModel):
    table_type: TableType


class TableCreate(TableBase):
    pass


class Table(TableBase):
    id: int

    class Config:
        orm_mode = True


class BookingBase(BaseModel):
    start_time: datetime
    end_time: datetime


class BookingCreate(BookingBase):
    user_id: int
    table_id: int

    @field_validator("start_time", "end_time")
    def check_datetimes(cls, v: datetime):
        if v.minute != 0 or v.second != 0 or v.microsecond != 0:
            raise HTTPException(status_code=400, detail="Time must be on the hour: e.g. 14:00 or 16:00")

        if v.replace(tzinfo=None) < datetime.now().replace(tzinfo=None):
            raise HTTPException(status_code=400, detail="Time must not be in the past")

        if not (9 <= v.hour < 21):
            raise HTTPException(status_code=400, detail="Booking must start and end between 9 AM and 9 PM")

        return v


class BookingShow(BookingBase):
    id: int
    user_id: int
    table_id: int

    class Config:
        orm_mode = True
