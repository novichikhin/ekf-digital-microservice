from sqlalchemy.ext.asyncio import AsyncSession

from ekf_digital_microservice.server.database.repositories.digest import DigestRepository
from ekf_digital_microservice.server.database.repositories.post import PostRepository
from ekf_digital_microservice.server.database.repositories.subscription import SubscriptionRepository
from ekf_digital_microservice.server.database.repositories.user import UserRepository


class DatabaseHolder:

    def __init__(self, session: AsyncSession):
        self.user = UserRepository(session=session)
        self.subscription = SubscriptionRepository(session=session)
        self.post = PostRepository(session=session)
        self.digest = DigestRepository(session=session)
