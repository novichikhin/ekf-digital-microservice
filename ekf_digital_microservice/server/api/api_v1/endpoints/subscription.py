from typing import Union

from fastapi import APIRouter, Depends
from starlette.status import HTTP_404_NOT_FOUND

from ekf_digital_microservice.server import schemas
from ekf_digital_microservice.server.api.api_v1 import responses
from ekf_digital_microservice.server.api.api_v1.dependencies.database import DatabaseHolderMarker
from ekf_digital_microservice.server.database.holder import DatabaseHolder
from ekf_digital_microservice.server.services.subscription import create_subscription, get_subscription

router = APIRouter()


@router.post(
    "/",
    response_model=schemas.Subscription,
    responses={
        HTTP_404_NOT_FOUND: {
            "model": Union[
                responses.UserNotFound,
                responses.SubscriptionNotFound
            ]
        }
    }
)
async def create(subscription: schemas.CreateSubscription, holder: DatabaseHolder = Depends(DatabaseHolderMarker)):
    return await create_subscription(subscription=subscription, holder=holder)


@router.get(
    "/{id}",
    response_model=schemas.Subscription,
    responses={
        HTTP_404_NOT_FOUND: {
            "description": "Subscription not found error",
            "model": responses.SubscriptionNotFound
        }
    }
)
async def read(id: int, holder: DatabaseHolder = Depends(DatabaseHolderMarker)):
    return await get_subscription(id=id, holder=holder)
