from fastapi import HTTPException, status, Header, Depends

from ekf_digital_microservice.common import types
from ekf_digital_microservice.server.api.api_v1.dependencies.setting import SettingsMarker


def check_is_rmq(
        rmq_token: str = Header(description="RabbitMQ Token"),
        settings: types.Settings = Depends(SettingsMarker)
) -> None:
    if rmq_token != settings.rabbitmq_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
