import strawberry
from sqlmodel import Session, select
from strawberry.fastapi import GraphQLRouter

from ..models import Pinch, engine


@strawberry.type
class PinchType:
    id: int
    wide: bool
    deep: bool
    weight: float
    duration: float


@strawberry.type
class Query:
    @strawberry.field
    def pinches() -> list[PinchType]:
        with Session(engine) as session:
            pinches = session.exec(select(Pinch)).all()
        return [
            PinchType(
                id=p.id,
                wide=p.wide,
                deep=p.deep,
                weight=p.weight,
                duration=p.duration,
            )
            for p in pinches
        ]


schema = strawberry.Schema(query=Query)
router = GraphQLRouter(schema)
