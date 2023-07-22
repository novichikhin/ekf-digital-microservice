from typing import Union

from fastapi import APIRouter, Depends
from starlette.status import HTTP_404_NOT_FOUND

from ekf_digital_microservice.server import schemas
from ekf_digital_microservice.server.api.api_v1 import responses
from ekf_digital_microservice.server.api.api_v1.dependencies.database import DatabaseHolderMarker
from ekf_digital_microservice.server.database.holder import DatabaseHolder
from ekf_digital_microservice.server.services.post import (
    create_post,
    get_post,
    get_posts_by_user_id
)

router = APIRouter()


@router.post(
    "/",
    response_model=schemas.Post,
    responses={
        HTTP_404_NOT_FOUND: {
            "model": Union[
                responses.SubscriptionNotFound,
                responses.PostNotFound
            ]
        }
    }
)
async def create(post: schemas.CreatePost, holder: DatabaseHolder = Depends(DatabaseHolderMarker)):
    return await create_post(post=post, holder=holder)


@router.get(
    "/{id}",
    response_model=schemas.Post,
    responses={
        HTTP_404_NOT_FOUND: {
            "description": "Post not found error",
            "model": responses.PostNotFound
        }
    }
)
async def read(id: int, holder: DatabaseHolder = Depends(DatabaseHolderMarker)):
    return await get_post(id=id, holder=holder)


@router.get("/by_user_id/{user_id}", response_model=list[schemas.Post])
async def read_all_by_user_id(user_id: int, holder: DatabaseHolder = Depends(DatabaseHolderMarker)):
    return await get_posts_by_user_id(user_id=user_id, holder=holder)
