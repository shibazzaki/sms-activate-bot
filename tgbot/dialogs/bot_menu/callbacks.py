from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from tgbot.config import Config
from tgbot.services.cryptopay_service import CryptoPayService
from tgbot.filters.admin import AdminFilter



# Check if the user is an admin
async def is_it_admin(dialog_manager, **kwargs):
    from_user = dialog_manager.event.from_user
    config: Config = dialog_manager.middleware_data["config"]
    is_user_admin = from_user.id in config.tg_bot.admin_ids
    return {"is_admin": is_user_admin}


# Handle payment processing
async def handle_payment(c, b, dialog_manager):
    user_id = dialog_manager.event.from_user.id
    session = dialog_manager.middleware_data["db_session"]
    cryptopay_service: CryptoPayService = dialog_manager.middleware_data["cryptopay_service"]

    # Create invoice
    invoice = await cryptopay_service.create_invoice(
        user_id=user_id,
        amount=100,  # Example amount
        session=session,
        asset='USDT',  # Example currency
        description="Payment for selected service"
    )

    await c.message.answer(f"Please pay using this link: {invoice.pay_url}")
    