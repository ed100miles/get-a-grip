from datetime import datetime

import jwt
import strawberry
from fastapi import Depends
from sqlmodel import Session, select
from strawberry.fastapi import BaseContext, GraphQLRouter

from ..dependencies import get_session, oauth2_scheme
from ..models import Pinch
from ..settings import settings
from .users import TokenData


class CustomContext(BaseContext):
    def __init__(self, session: Session, token_data: TokenData | None = None):
        self.session = session
        self.token_data = token_data


def create_context(
    token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)
):
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    token_data = TokenData.model_validate(payload)
    return CustomContext(session=session, token_data=token_data)


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
class Mutation:
    @strawberry.mutation()
    def add_pinch(
        self,
        wide: bool,
        deep: bool,
        weight: float,
        duration: float,
        info: strawberry.Info,
    ) -> PinchType:
        session: Session = info.context.session
        user_id = info.context.token_data.user_id
        pinch = Pinch(
            user_id=user_id,
            wide=wide,
            deep=deep,
            weight=weight,
            duration=duration,
        )
        session.add(pinch)
        session.commit()
        session.refresh(pinch)

        return PinchType(
            id=pinch.id,
            user_id=pinch.user_id,
            wide=pinch.wide,
            deep=pinch.deep,
            weight=pinch.weight,
            duration=pinch.duration,
            created_at=pinch.created_at,
        )


@strawberry.type
class Query:
    @strawberry.field
    def pinches(
        self,
        info: strawberry.Info,
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
        session: Session = info.context.session
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


schema = strawberry.Schema(query=Query, mutation=Mutation)
router = GraphQLRouter(
    schema,
    context_getter=create_context,
)
