from ekf_digital_microservice.server.api.api_v1.responses.main import BaseResponse


class DigestNotFound(BaseResponse):
    detail: str = "Digest not found"
