from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette import status

from ekf_digital_microservice.server import exceptions
from ekf_digital_microservice.server.exceptions.main import BaseAppException


def register_exceptions(app: FastAPI) -> None:
    app.add_exception_handler(exceptions.UserNotFound, user_not_found_handler)
    app.add_exception_handler(exceptions.SubscriptionNotFound, subscription_not_found_handler)
    app.add_exception_handler(exceptions.PostNotFound, post_not_found_handler)
    app.add_exception_handler(exceptions.DigestNotFound, digest_not_found_handler)


async def user_not_found_handler(_, err: exceptions.UserNotFound) -> ORJSONResponse:
    return await handle_error(err, status_code=status.HTTP_404_NOT_FOUND)


async def subscription_not_found_handler(_, err: exceptions.SubscriptionNotFound) -> ORJSONResponse:
    return await handle_error(err, status_code=status.HTTP_404_NOT_FOUND)


async def post_not_found_handler(_, err: exceptions.PostNotFound) -> ORJSONResponse:
    return await handle_error(err, status_code=status.HTTP_404_NOT_FOUND)


async def digest_not_found_handler(_, err: exceptions.DigestNotFound) -> ORJSONResponse:
    return await handle_error(err, status_code=status.HTTP_404_NOT_FOUND)


async def handle_error(err: BaseAppException, status_code: int) -> ORJSONResponse:
    return ORJSONResponse({"status": "fail", "detail": err.message}, status_code=status_code)
