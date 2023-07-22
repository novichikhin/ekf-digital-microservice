from pydantic import BaseModel

from ekf_digital_microservice.server import dto, enums


class BasePost(BaseModel):
    subscription_id: int
    body: str
    popularity: enums.Popularity


class Post(BasePost):
    id: int

    @classmethod
    def from_dto(cls, post: dto.Post) -> "Post":
        return Post(
            id=post.id,
            subscription_id=post.subscription_id,
            body=post.body,
            popularity=post.popularity
        )


class CreatePost(BasePost):
    pass
