import datetime
from typing import Final

from faker import Faker
from sqlmodel import Session

from .dependencies import get_session
from .models import Pinch, User
from .routers.users import pwd_context

fake = Faker()
Faker.seed(1234)

NUM_SEED_PINCHES_PER_USER: Final = 100

seed_users = [
    User(
        username=fake.user_name(),
        email=fake.email(),
        hashed_password=pwd_context.hash(fake.password()),
        email_validated=True,
    )
    for _ in range(10)
] + [
    User(
        username="test",
        email="test@mail.com",
        hashed_password=pwd_context.hash("test"),
        email_validated=True,
    ),
    User(
        username="test2",
        email="test2@mail.com",
        hashed_password=pwd_context.hash("test2"),
        email_validated=False,
    ),
]


def seed_db(session: Session, seed_users=seed_users):
    # Create 10 users + 1 test user

    session.add_all(seed_users)
    session.commit()
    for user in seed_users:
        session.refresh(user)

    # create some pinches for the users
    seed_pinches = []
    base_time = fake.date_time_between(start_date="-1y", end_date="now")
    for user in seed_users:
        for num in range(NUM_SEED_PINCHES_PER_USER):
            seed_pinches.append(
                Pinch(
                    wide=fake.boolean(),
                    deep=fake.boolean(),
                    weight=fake.random.uniform(num * 0.99, num * 1.01),
                    duration=fake.random.uniform(20, 60),
                    user_id=user.id,
                    created_at=base_time
                    + datetime.timedelta(days=num * fake.random.uniform(0.9, 1.1)),
                )
            )
    session.add_all(seed_pinches)
    session.commit()


if __name__ == "__main__":
    input("This will seed the database in your settings.py, Press enter to continue.")
    session = next(get_session())
    seed_db(session)
    session.close()
