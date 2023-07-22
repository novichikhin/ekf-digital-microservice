from ekf_digital_microservice.server.exceptions.main import BaseAppException


class PostNotFound(BaseAppException):

    @property
    def message(self) -> str:
        return "Post not found"
