from typing import Optional, TYPE_CHECKING

from marshmallow.fields import Decimal
from sqlalchemy import ForeignKey
from enum import Enum

from sqlalchemy.dialects.mysql import DECIMAL
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import Base, TableNameMixin, TimestampMixin, int_pk


if TYPE_CHECKING:
    from .users import User

class TransactionType(Enum):
    TOPUP = "topup"
    EXPENDITURE = "expenditure"

class Transaction(Base, TimestampMixin, TableNameMixin):
    transaction_id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    amount: Mapped[Decimal] = mapped_column(DECIMAL(16, 8))
    type: Mapped[TransactionType]
    description: Mapped[Optional[str]]

    user: Mapped["User"] = relationship("User", back_populates="transactions")
