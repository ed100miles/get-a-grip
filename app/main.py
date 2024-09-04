from fastapi import FastAPI

from .routers import graphql_route, pinches, users

app = FastAPI()
app.include_router(users.router)
app.include_router(pinches.router)
app.include_router(graphql_route.router, prefix="/graphql")