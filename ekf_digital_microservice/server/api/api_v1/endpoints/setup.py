from fastapi import FastAPI

from ekf_digital_microservice.server.api.api_v1.endpoints import (
    user,
    subscription,
    post,
    digest,
    healthcheck
)


def register_routers(app: FastAPI) -> None:
    app.include_router(
        user.router,
        prefix="/user",
        tags=["user"]
    )

    app.include_router(
        subscription.router,
        prefix="/subscription",
        tags=["subscription"]
    )

    app.include_router(
        post.router,
        prefix="/post",
        tags=["post"]
    )

    app.include_router(
        digest.router,
        prefix="/digest",
        tags=["digest"]
    )

    app.include_router(
        healthcheck.router,
        prefix="/healthcheck",
        tags=["healthcheck"]
    )
