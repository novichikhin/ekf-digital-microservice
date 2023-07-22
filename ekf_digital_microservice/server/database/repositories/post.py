import sqlalchemy as sa

from typing import Optional, Sequence

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from ekf_digital_microservice.server import exceptions, dto, enums
from ekf_digital_microservice.server.database import models
from ekf_digital_microservice.server.database.repositories.main import Repository


class PostRepository(Repository[models.Post]):

    def __init__(self, session: AsyncSession):
        super().__init__(model=models.Post, session=session)

    async def read_by_id(self, id: int) -> Optional[dto.Post]:
        post = await self._read_by_id(id=id)

        if not post:
            raise exceptions.PostNotFound

        return post.to_dto()

    async def read_all_by_user_id(self, user_id: int) -> list[dto.Post]:
        stmt = sa.select(models.Post).join(
            models.Subscription,
            sa.and_(
                models.Subscription.id == models.Post.subscription_id,
                models.Subscription.user_id == user_id
            )
        )

        result: sa.ScalarResult[models.Post] = await self._session.scalars(
            sa.select(models.Post).from_statement(stmt)
        )
        await self._session.commit()

        posts: Sequence[models.Post] = result.all()

        return [post.to_dto() for post in posts]

    async def create(
            self,
            subscription_id: int,
            body: str,
            popularity: enums.Popularity
    ) -> Optional[dto.Post]:
        stmt = insert(models.Post).values(
            subscription_id=subscription_id,
            body=body,
            popularity=popularity
        ).returning(models.Post)

        result: sa.ScalarResult[models.Post] = await self._session.scalars(
            sa.select(models.Post).from_statement(stmt)
        )
        await self._session.commit()

        post: Optional[models.Post] = result.one_or_none()

        if not post:
            raise exceptions.PostNotFound

        return post.to_dto()
