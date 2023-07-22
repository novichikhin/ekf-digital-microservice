from ekf_digital_microservice.server.api.api_v1.responses.main import BaseResponse


class SubscriptionNotFound(BaseResponse):
    detail: str = "Subscription not found"
