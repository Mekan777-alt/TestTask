from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class Admin(Base):
    __tablename__ = 'admin'

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)

