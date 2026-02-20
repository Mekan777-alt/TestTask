from database.base import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String


class Tag(Base):
    __tablename__ = 'tags'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
