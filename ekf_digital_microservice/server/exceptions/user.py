from ekf_digital_microservice.server.exceptions.main import BaseAppException


class UserNotFound(BaseAppException):

    @property
    def message(self) -> str:
        return "User not found"
