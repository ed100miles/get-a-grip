from fastapi import FastAPI, Depends

from .routers import graphql, pinches, users

app = FastAPI()
app.include_router(users.router, prefix="/user")
app.include_router(pinches.router, prefix="/pinch")
app.include_router(
    graphql.router, prefix="/graphql", dependencies=[Depends(users.oauth2_scheme)]
)
