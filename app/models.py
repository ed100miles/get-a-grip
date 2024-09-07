from datetime import UTC, datetime

from sqlmodel import Field, Relationship, SQLModel, create_engine

sqlite_url = "sqlite:///db.db"
engine = create_engine(sqlite_url, echo=True)


class UserBase(SQLModel):
    username: str
    email: str


class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    hashed_password: str
    pinches: list["Pinch"] = Relationship(back_populates="user")
    created_at: datetime = Field(default_factory=datetime.now)


class UserCreate(UserBase):
    password: str


class UserPublic(UserBase):
    id: int
    created_at: datetime


class PinchCreate(SQLModel):
    wide: bool
    deep: bool
    weight: float
    duration: float


class Pinch(PinchCreate, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="pinches")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_db_and_tables()
