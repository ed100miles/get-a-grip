from datetime import datetime

import strawberry
from sqlmodel import Session, select
from strawberry.fastapi import GraphQLRouter

from ..models import Pinch, engine


@strawberry.type
class PinchType:
    id: int
    user_id: int
    wide: bool
    deep: bool
    weight: float
    duration: float
    created_at: datetime


@strawberry.type
class Query:
    @strawberry.field
    def pinches(
        self,
        user_id: int | None = None,
        wide: bool | None = None,
        deep: bool | None = None,
        min_weight: float | None = None,
        max_weight: float | None = None,
        min_duration: float | None = None,
        max_duration: float | None = None,
        created_after: datetime | None = None,
        created_before: datetime | None = None,
    ) -> list[PinchType]:
        with Session(engine) as session:
            statement = select(Pinch)
            if user_id is not None:
                statement = statement.where(Pinch.user_id == user_id)
            if wide is not None:
                statement = statement.where(Pinch.wide == wide)
            if deep is not None:
                statement = statement.where(Pinch.deep == deep)
            if min_weight is not None:
                statement = statement.where(Pinch.weight >= min_weight)
            if max_weight is not None:
                statement = statement.where(Pinch.weight <= max_weight)
            if min_duration is not None:
                statement = statement.where(Pinch.duration >= min_duration)
            if max_duration is not None:
                statement = statement.where(Pinch.duration <= max_duration)
            if created_after is not None:
                statement = statement.where(Pinch.created_at >= created_after)
            if created_before is not None:
                statement = statement.where(Pinch.created_at <= created_before)
            pinches = session.exec(statement).all()
        return [
            PinchType(
                id=p.id,
                user_id=p.user_id,
                wide=p.wide,
                deep=p.deep,
                weight=p.weight,
                duration=p.duration,
                created_at=p.created_at,
            )
            for p in pinches
        ]


schema = strawberry.Schema(query=Query)
router = GraphQLRouter(schema)
