from aiohttp import web
from aiocryptopay.models.update import Update
from tgbot.services.cryptopay_service import CryptoPayService

async def webhook_handler(request: web.Request):
    cryptopay_service: CryptoPayService = request.app['cryptopay_service']
    session = request.app['db_session']
    body = await request.json()
    signature = request.headers.get("Crypto-Pay-Api-Signature")

    if cryptopay_service.client.check_signature(str(body), signature):
        update = Update(**body)
        # Process the payment update
        await cryptopay_service.update_transaction_status(update.invoice_id, "paid", session)
        return web.Response(text="OK")
    else:
        return web.Response(status=400, text="Invalid signature")
