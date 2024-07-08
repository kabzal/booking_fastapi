from fastapi import FastAPI

from routers import bookings, users, tables
from auth import auth


app = FastAPI(
    title="Happy Coon Coffee tables reservation service",
)

app.include_router(bookings.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tables.router)


@app.get("/")
async def read_root():
    return {"message": "Welcome to Happy Coon Coffee tables reservation service!"}
