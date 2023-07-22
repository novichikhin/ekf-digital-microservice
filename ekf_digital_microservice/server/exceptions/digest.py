from ekf_digital_microservice.server.exceptions.main import BaseAppException


class DigestNotFound(BaseAppException):

    @property
    def message(self) -> str:
        return "Digest not found"
