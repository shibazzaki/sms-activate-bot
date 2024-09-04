from aiocryptopay import AioCryptoPay, Networks
from aiocryptopay.models.invoice import Invoice
from aiocryptopay.models.update import Update
from aiocryptopay.models.transfer import Transfer
from aiocryptopay.models.check import Check, CheckStatus
from sqlalchemy.orm import Session
from infrastructure.database.models import Transaction


class CryptoPayService:
    def __init__(self, api_key: str, network: str = Networks.MAIN_NET):
        self.client = AioCryptoPay(token=api_key, network=network)

    async def create_invoice(self, user_id: int, amount: float, session: Session, asset: str = 'USDT',
                             description: str = None) -> Invoice:
        invoice = await self.client.create_invoice(
            amount=amount,
            asset=asset,
            description=description
        )

        transaction = Transaction(
            user_id=user_id,
            invoice_id=invoice.invoice_id,
            amount=amount,
            status="pending",
            hash=invoice.hash,
            asset=asset,
            bot_invoice_url=invoice.pay_url,
            description=description,
            expiration_date=invoice.expiration_date,
        )
        session.add(transaction)
        session.commit()

        return invoice

    async def update_transaction_status(self, invoice_id: int, status: str, session: Session):
        transaction = session.query(Transaction).filter_by(invoice_id=invoice_id).first()
        if transaction:
            transaction.status = status
            session.commit()

    async def get_balance(self):
        return await self.client.get_balance()

    async def get_currencies(self):
        return await self.client.get_currencies()

    async def get_exchange_rates(self):
        return await self.client.get_exchange_rates()
