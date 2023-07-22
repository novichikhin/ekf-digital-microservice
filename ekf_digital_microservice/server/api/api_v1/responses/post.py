from ekf_digital_microservice.server.api.api_v1.responses.main import BaseResponse


class PostNotFound(BaseResponse):
    detail: str = "Post not found"
