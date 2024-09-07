from fastapi import Depends, FastAPI

from .dependencies import oauth2_scheme
from .routers import graphql, pinches, users

app = FastAPI()
app.include_router(users.router, prefix="/user")
app.include_router(pinches.router, prefix="/pinch")
app.include_router(
    graphql.router, prefix="/graphql", dependencies=[Depends(oauth2_scheme)]
)


@app.get("/")
async def root():
    return {"message": "get-a-grip-api - create an account or login to access the API"}
