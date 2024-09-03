from fastapi import FastAPI

from .routers import users, pinches

app = FastAPI()
app.include_router(users.router)
app.include_router(pinches.router)
