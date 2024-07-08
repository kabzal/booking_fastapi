from datetime import datetime

from sqlalchemy import Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column

from models.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )
    username: Mapped[str] = mapped_column(
        String,
        unique=True,
        index=True
    )
    email: Mapped[str] = mapped_column(
        String,
        unique=True,
        index=True
    )
    hashed_password: Mapped[str] = mapped_column(String)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    disabled: Mapped[bool] = mapped_column(Boolean, default=False)

    bookings: Mapped[list["Booking"]] = relationship(back_populates="user")


class Table(Base):
    __tablename__ = "tables"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )
    table_type: Mapped[str] = mapped_column(String)

    bookings: Mapped[list["Booking"]] = relationship(back_populates="table",
                                                     cascade="all, delete-orphan")


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )
    start_time: Mapped[datetime] = mapped_column(DateTime)
    end_time: Mapped[datetime] = mapped_column(DateTime)

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id")
    )
    user: Mapped["User"] = relationship(back_populates="bookings")
    table_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("tables.id", ondelete="CASCADE")
    )
    table: Mapped["Table"] = relationship(back_populates="bookings")

