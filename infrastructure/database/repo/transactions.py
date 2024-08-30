from cgitb import reset
from typing import Optional

from sqlalchemy.dialects.postgresql import insert

from infrastructure.database.models import Transaction
from infrastructure.database.models.transaction import TransactionType
from infrastructure.database.repo.base import BaseRepo


class TransactionRepo(BaseRepo):
    async def create_transaction(
            self,
            user_id: int,
            amount: float,
            type: TransactionType,
            description: Optional[str] = None,
    ):
         insert_stmt = (
             insert(Transaction)
             .values(
                 user_id=user_id,
                 amount=amount,
                 type=type,
                 description=description,
             )
             .returning(Transaction)
         )
         result = await self.session.execute(insert_stmt)

         await self.session.commit()
         return result.scalar_one()