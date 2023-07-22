import sqlalchemy as sa
import sqlalchemy.orm as so

from ekf_digital_microservice.server import dto
from ekf_digital_microservice.server.database.models.main import DatabaseBase


class Subscription(DatabaseBase):
    __tablename__ = "subscriptions"

    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    source_name: so.Mapped[str] = so.mapped_column(nullable=False)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    def to_dto(self) -> dto.Subscription:
        return dto.Subscription(
            id=self.id,
            source_name=self.source_name,
            user_id=self.user_id
        )
