from pydantic import BaseModel

from ekf_digital_microservice.server import dto


class BaseDigest(BaseModel):
    post_id: int


class Digest(BaseDigest):
    id: int

    @classmethod
    def from_dto(cls, digest: dto.Digest) -> "Digest":
        return Digest(id=digest.id, post_id=digest.post_id)


class CreateDigest(BaseDigest):
    pass
