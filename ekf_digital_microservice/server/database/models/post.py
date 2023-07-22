import sqlalchemy as sa
import sqlalchemy.orm as so

from ekf_digital_microservice.server import dto, enums
from ekf_digital_microservice.server.database.models.main import DatabaseBase


class Post(DatabaseBase):
    __tablename__ = "posts"

    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)

    subscription_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("subscriptions.id", ondelete="CASCADE"),
        nullable=False
    )

    body: so.Mapped[str] = so.mapped_column(nullable=False)
    popularity: so.Mapped[enums.Popularity] = so.mapped_column(sa.Enum(enums.Popularity), nullable=False)

    def to_dto(self) -> dto.Post:
        return dto.Post(
            id=self.id,
            subscription_id=self.subscription_id,
            body=self.body,
            popularity=self.popularity
        )
