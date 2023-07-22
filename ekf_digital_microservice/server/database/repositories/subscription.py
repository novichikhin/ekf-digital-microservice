import sqlalchemy as sa

from typing import Optional

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from ekf_digital_microservice.server import exceptions, dto
from ekf_digital_microservice.server.database import models
from ekf_digital_microservice.server.database.repositories.main import Repository


class SubscriptionRepository(Repository[models.Subscription]):

    def __init__(self, session: AsyncSession):
        super().__init__(model=models.Subscription, session=session)

    async def read_by_id(self, id: int) -> Optional[dto.Subscription]:
        subscription = await self._read_by_id(id=id)

        if not subscription:
            raise exceptions.SubscriptionNotFound

        return subscription.to_dto()

    async def create(
            self,
            source_name: str,
            user_id: int
    ) -> Optional[dto.Subscription]:
        stmt = insert(models.Subscription).values(
            source_name=source_name,
            user_id=user_id
        ).returning(models.Subscription)

        result: sa.ScalarResult[models.Subscription] = await self._session.scalars(
            sa.select(models.Subscription).from_statement(stmt)
        )
        await self._session.commit()

        subscription: Optional[models.Subscription] = result.one_or_none()

        if not subscription:
            raise exceptions.SubscriptionNotFound

        return subscription.to_dto()
