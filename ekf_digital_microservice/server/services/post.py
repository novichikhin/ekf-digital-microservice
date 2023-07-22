from ekf_digital_microservice.server import schemas
from ekf_digital_microservice.server.database.holder import DatabaseHolder


async def create_post(
        *,
        post: schemas.CreatePost,
        holder: DatabaseHolder
) -> schemas.Post:
    subscription = await holder.subscription.read_by_id(id=post.subscription_id)

    post = await holder.post.create(
        subscription_id=subscription.id,
        body=post.body,
        popularity=post.popularity
    )

    return schemas.Post.from_dto(post=post)


async def get_post(
        *,
        id: int,
        holder: DatabaseHolder
) -> schemas.Post:
    post = await holder.post.read_by_id(id=id)

    return schemas.Post.from_dto(post=post)


async def get_posts_by_user_id(
        *,
        user_id: int,
        holder: DatabaseHolder
) -> list[schemas.Post]:
    posts = await holder.post.read_all_by_user_id(user_id=user_id)

    return [schemas.Post.from_dto(post=post) for post in posts]
