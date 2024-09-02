from sqlmodel import SQLModel, Field, create_engine

sqlite_url = "sqlite:///db.db"
engine = create_engine(sqlite_url, echo=True)


class UserBase(SQLModel):
    username: str
    email: str


class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    hashed_password: str


class UserCreate(UserBase):
    password: str


class UserPublic(UserBase):
    id: int


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_db_and_tables()
