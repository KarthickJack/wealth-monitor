from sqlalchemy import SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TransactionType(Base):
    __tablename__ = "transaction_types"

    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
