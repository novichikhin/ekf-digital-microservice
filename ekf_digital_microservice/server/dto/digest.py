from dataclasses import dataclass


@dataclass
class BaseDigest:
    post_id: int


@dataclass
class Digest(BaseDigest):
    id: int


@dataclass
class CreateDigest(BaseDigest):
    pass
