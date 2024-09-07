from faker import Faker
from sqlmodel import Session

from app.models import Pinch, User, engine
from app.routers.users import pwd_context

fake = Faker()
Faker.seed(1234)

if __name__ == "__main__":
    with Session(engine) as session:
        # Create 10 users
        seed_users = [
            User(
                username=fake.user_name(),
                email=fake.email(),
                hashed_password=pwd_context.hash(fake.password()),
            )
            for _ in range(10)
        ] + [
            User(
                username="test",
                email="test@mail.com",
                hashed_password=pwd_context.hash("test"),
            )
        ]
        session.add_all(seed_users)
        session.commit()
        for user in seed_users:
            session.refresh(user)

        # create some pinches for the users
        seed_pinches = []
        for user in seed_users:
            for _ in range(100):
                seed_pinches.append(
                    Pinch(
                        wide=fake.boolean(),
                        deep=fake.boolean(),
                        weight=fake.random.uniform(0.01, 10),
                        duration=fake.random.uniform(0.01, 10),
                        user_id=user.id,
                    )
                )
        session.add_all(seed_pinches)
        session.commit()

