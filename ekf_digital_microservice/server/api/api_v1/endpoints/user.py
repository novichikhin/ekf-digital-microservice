from fastapi import APIRouter, Depends
from starlette.status import HTTP_404_NOT_FOUND

from ekf_digital_microservice.server import schemas
from ekf_digital_microservice.server.api.api_v1 import responses
from ekf_digital_microservice.server.api.api_v1.dependencies.database import DatabaseHolderMarker
from ekf_digital_microservice.server.database.holder import DatabaseHolder
from ekf_digital_microservice.server.services.user import create_user, get_user

router = APIRouter()


@router.post(
    "/",
    response_model=schemas.User,
    responses={
        HTTP_404_NOT_FOUND: {
            "description": "User not found error",
            "model": responses.UserNotFound
        }
    }
)
async def create(user: schemas.CreateUser, holder: DatabaseHolder = Depends(DatabaseHolderMarker)):
    return await create_user(user=user, holder=holder)


@router.get(
    "/{id}",
    response_model=schemas.User,
    responses={
        HTTP_404_NOT_FOUND: {
            "description": "User not found error",
            "model": responses.UserNotFound
        }
    }
)
async def read(id: int, holder: DatabaseHolder = Depends(DatabaseHolderMarker)):
    return await get_user(id=id, holder=holder)
