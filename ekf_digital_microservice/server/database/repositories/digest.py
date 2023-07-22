from dataclasses import asdict

import sqlalchemy as sa

from typing import Optional, Sequence

from sqlalchemy import Result
from sqlalchemy.exc import IntegrityError, DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession

from ekf_digital_microservice.server import exceptions, dto
from ekf_digital_microservice.server.database import models
from ekf_digital_microservice.server.database.repositories.main import Repository


class DigestRepository(Repository[models.Digest]):

    def __init__(self, session: AsyncSession):
        super().__init__(model=models.Digest, session=session)

    async def read_by_id(self, id: int) -> Optional[dto.Digest]:
        digest = await self._read_by_id(id=id)

        if not digest:
            raise exceptions.DigestNotFound

        return digest.to_dto()

    async def create(self, create_digests: list[dto.CreateDigest]) -> list[dto.Digest]:
        stmt = sa.insert(models.Digest).returning(models.Digest)
        try:
            result: Result[list[models.Digest]] = await self._session.execute(
                sa.select(models.Digest).from_statement(stmt),
                [asdict(create_digest) for create_digest in create_digests]
            )
            await self._session.commit()
        except IntegrityError as e:
            await self._session.rollback()
            self._parse_create_error(err=e)
        else:
            digests: Sequence[models.Digest] = result.scalars().all()

            return [digest.to_dto() for digest in digests]

    def _parse_create_error(self, err: DBAPIError) -> None:
        constraint_name = err.__cause__.__cause__.constraint_name  # type: ignore

        if constraint_name == "digests_post_id_fkey":
            raise exceptions.PostNotFound from err
