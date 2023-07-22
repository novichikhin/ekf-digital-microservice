from pydantic import BaseModel

from ekf_digital_microservice.server import dto


class BaseUser(BaseModel):
    name: str


class User(BaseUser):
    id: int

    @classmethod
    def from_dto(cls, user: dto.User) -> "User":
        return User(id=user.id, name=user.name)


class CreateUser(BaseUser):
    pass
