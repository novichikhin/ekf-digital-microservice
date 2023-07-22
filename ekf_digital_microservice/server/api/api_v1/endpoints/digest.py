from aio_pika.abc import AbstractChannel
from fastapi import APIRouter, Depends
from starlette.status import HTTP_404_NOT_FOUND, HTTP_200_OK

from ekf_digital_microservice.server import schemas
from ekf_digital_microservice.server.api.api_v1 import responses
from ekf_digital_microservice.server.api.api_v1.dependencies.database import DatabaseHolderMarker
from ekf_digital_microservice.server.api.api_v1.dependencies.rabbitmq import RMQChannelMarker
from ekf_digital_microservice.server.core.security import check_is_rmq
from ekf_digital_microservice.server.database.holder import DatabaseHolder
from ekf_digital_microservice.server.services.digest import (
    create_digests,
    get_digest,
    generate_digests
)

router = APIRouter()


@router.post(
    "/",
    response_model=list[schemas.Digest],
    responses={
        HTTP_404_NOT_FOUND: {
            "description": "Post not found error",
            "model": responses.PostNotFound
        }
    },
    dependencies=[Depends(check_is_rmq)]
)
async def create(digests: list[schemas.CreateDigest], holder: DatabaseHolder = Depends(DatabaseHolderMarker)):
    return await create_digests(digests=digests, holder=holder)


@router.get(
    "/{id}",
    response_model=schemas.Digest,
    responses={
        HTTP_404_NOT_FOUND: {
            "description": "Digest not found error",
            "model": responses.DigestNotFound
        }
    }
)
async def read(id: int, holder: DatabaseHolder = Depends(DatabaseHolderMarker)):
    return await get_digest(id=id, holder=holder)


@router.post(
    "/generate/{user_id}",
    status_code=HTTP_200_OK,
    responses={
        HTTP_404_NOT_FOUND: {
            "description": "User not found error",
            "model": responses.UserNotFound
        }
    }
)
async def generate(
        user_id: int,
        holder: DatabaseHolder = Depends(DatabaseHolderMarker),
        rmq_channel: AbstractChannel = Depends(RMQChannelMarker)
):
    await generate_digests(
        user_id=user_id,
        holder=holder,
        rmq_channel=rmq_channel
    )
