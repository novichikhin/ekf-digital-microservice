import sqlalchemy as sa
import sqlalchemy.orm as so

from ekf_digital_microservice.server import dto
from ekf_digital_microservice.server.database.models.main import DatabaseBase


class Digest(DatabaseBase):
    __tablename__ = "digests"

    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    post_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)

    def to_dto(self) -> dto.Digest:
        return dto.Digest(id=self.id, post_id=self.post_id)
