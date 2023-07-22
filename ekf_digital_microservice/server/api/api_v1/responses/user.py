from ekf_digital_microservice.server.api.api_v1.responses.main import BaseResponse


class UserNotFound(BaseResponse):
    detail: str = "User not found"
