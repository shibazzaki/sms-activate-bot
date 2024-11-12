from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from infrastructure.database.models import User
from tgbot.config import Config
from tgbot.services.cryptopay_service import CryptoPayService
from tgbot.filters.admin import AdminFilter
from sqlalchemy.orm import Session
from infrastructure.database.models.transaction import Transaction

# Check if the user is an admin
async def is_it_admin(dialog_manager, **kwargs):
    from_user = dialog_manager.event.from_user
    config: Config = dialog_manager.middleware_data["config"]
    is_user_admin = from_user.id in config.tg_bot.admin_ids
    return {"is_admin": is_user_admin}

async def handle_payment(dialog_manager: DialogManager):
    """
    Створює інвойс для поповнення балансу на основі суми та валюти, вибраних користувачем.
    """
    user_id = dialog_manager.event.from_user.id
    session: Session = dialog_manager.middleware_data["db_session"]
    cryptopay_service: CryptoPayService = dialog_manager.middleware_data["cryptopay_service"]

    # Отримання даних від користувача
    amount = dialog_manager.dialog_data.get("amount")
    currency = dialog_manager.dialog_data.get("currency")

    if not amount or not currency:
        await dialog_manager.event.message.answer("Please enter an amount and select a currency.")
        return

    # Створення інвойсу
    invoice = await cryptopay_service.create_invoice(
        user_id=user_id,
        amount=amount,
        session=session,
        asset=currency,  # Використання вибраної валюти
        description=f"Top-up balance ({amount} {currency})"
    )

    # Надсилання посилання на оплату
    await dialog_manager.event.message.answer(f"Please pay using this link: {invoice}")


async def check_payment_status(c: CallbackQuery, button, dialog_manager: DialogManager):
    user_id = dialog_manager.event.from_user.id
    session: Session = dialog_manager.middleware_data["db_session"]
    cryptopay_service: CryptoPayService = dialog_manager.middleware_data["cryptopay_service"]

    # Знаходження транзакції зі статусом "pending"
    transaction = session.query(Transaction).filter_by(user_id=user_id, status="pending").first()

    if not transaction:
        await c.message.answer("У вас немає очікуючих оплат.")
        return

    # Перевірка статусу оплати
    await cryptopay_service.check_and_update_payment_status(invoice_id=transaction.invoice_id, session=session)

    # Оновлення балансу користувача після успішної оплати
    updated_transaction = session.query(Transaction).filter_by(invoice_id=transaction.invoice_id).first()
    if updated_transaction.status == "completed":
        user = session.query(User).filter_by(user_id=user_id).first()
        if user:
            user.balance += float(updated_transaction.amount)  # Оновлення балансу
            session.commit()  # Збереження змін
            await c.message.answer("Оплата успішно підтверджена! Ваш баланс поповнено.")
        else:
            await c.message.answer("Помилка: користувач не знайдений.")
    else:
        await c.message.answer("Оплата ще не підтверджена або не виконана.")
