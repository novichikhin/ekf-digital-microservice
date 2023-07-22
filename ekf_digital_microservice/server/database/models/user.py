import sqlalchemy.orm as so

from ekf_digital_microservice.server import dto
from ekf_digital_microservice.server.database.models.main import DatabaseBase


class User(DatabaseBase):
    __tablename__ = "users"

    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    name: so.Mapped[str] = so.mapped_column(nullable=False)

    def to_dto(self) -> dto.User:
        return dto.User(id=self.id, name=self.name)
