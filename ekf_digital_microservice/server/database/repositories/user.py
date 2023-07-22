import sqlalchemy as sa

from typing import Optional

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from ekf_digital_microservice.server import exceptions, dto
from ekf_digital_microservice.server.database import models
from ekf_digital_microservice.server.database.repositories.main import Repository


class UserRepository(Repository[models.User]):

    def __init__(self, session: AsyncSession):
        super().__init__(model=models.User, session=session)

    async def read_by_id(self, id: int) -> Optional[dto.User]:
        user = await self._read_by_id(id=id)

        if not user:
            raise exceptions.UserNotFound

        return user.to_dto()

    async def create(self, name: str) -> Optional[dto.User]:
        stmt = insert(models.User).values(name=name).returning(models.User)

        result: sa.ScalarResult[models.User] = await self._session.scalars(
            sa.select(models.User).from_statement(stmt)
        )
        await self._session.commit()

        user: Optional[models.User] = result.one_or_none()

        if not user:
            raise exceptions.UserNotFound

        return user.to_dto()
