from ekf_digital_microservice.server.exceptions.main import BaseAppException


class SubscriptionNotFound(BaseAppException):

    @property
    def message(self) -> str:
        return "Subscription not found"
