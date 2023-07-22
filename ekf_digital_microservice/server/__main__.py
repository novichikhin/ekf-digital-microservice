import asyncio
import logging

import uvicorn

from ekf_digital_microservice.common import types
from ekf_digital_microservice.server.api.setup import register_app


def run_application() -> None:
    settings = types.Settings()
    app = register_app(settings=settings)

    config = uvicorn.Config(
        app,
        host=settings.server_host,
        port=settings.server_port,
        reload=True,
        log_level=logging.INFO
    )

    server = uvicorn.Server(config)

    asyncio.run(server.serve())


if __name__ == "__main__":
    run_application()
