from aiocryptopay import AioCryptoPay, Networks
from sqlalchemy.orm import Session
from infrastructure.database.models.transaction import Transaction
from infrastructure.database.models.users import User

class CryptoPayService:
    def __init__(self, api_key: str, network: str = Networks.MAIN_NET):
        self.client = AioCryptoPay(token=api_key, network=network)

    async def create_invoice(self, user_id: int, amount_usd: float, session: Session, asset: str = 'USDT') -> str:
        """
        Створює інвойс для поповнення балансу в доларах, оплата у USDT.
        :param user_id: Ідентифікатор користувача.
        :param amount_usd: Сума поповнення в доларах.
        :param session: Сесія бази даних.
        :param asset: Валюта для отримання платежу (за замовчуванням 'USDT').
        :return: Посилання на оплату.
        """
        try:
            # Створення інвойсу
            invoice = await self.client.create_invoice(
                amount=amount_usd,
                asset=asset,
                description=f"Поповнення балансу користувача {user_id}"
            )

            # Збереження транзакції в базі даних
            transaction = Transaction(
                user_id=user_id,
                invoice_id=invoice.invoice_id,
                amount=amount_usd,
                status="pending",
                hash=invoice.hash,
                asset=asset,
                bot_invoice_url=invoice.pay_url,
                description=f"Поповнення балансу для користувача {user_id}",
                expiration_date=invoice.expiration_date,
            )
            session.add(transaction)
            session.commit()

            return invoice.pay_url
        except Exception as e:
            print(f"Помилка створення інвойсу: {e}")
            return None

    async def check_and_update_payment_status(self, invoice_id: str, session: Session):
        """
        Перевіряє статус оплати інвойсу та оновлює статус транзакції в базі.
        :param invoice_id: Ідентифікатор інвойсу.
        :param session: Сесія бази даних.
        """
        try:
            invoice_status = await self.client.get_invoice(invoice_id=invoice_id)

            if invoice_status.status == 'paid':
                transaction = session.query(Transaction).filter_by(invoice_id=invoice_id).first()
                if transaction and transaction.status != 'completed':
                    transaction.status = 'completed'

                    # Оновлення балансу користувача
                    user = session.query(User).filter_by(user_id=transaction.user_id).first()
                    if user:
                        user.balance += transaction.amount  # Додавання суми в доларах до балансу користувача

                    session.commit()
                    print(f"Транзакція {invoice_id} успішно завершена.")
            else:
                print(f"Статус інвойсу {invoice_id}: {invoice_status.status}")
        except Exception as e:
            print(f"Помилка перевірки статусу інвойсу: {e}")
