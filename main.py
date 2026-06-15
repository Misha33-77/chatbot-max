import asyncio
import logging
from aiohttp import web
from maxapi import Bot
from maxapi.types import UpdateType
from config import BOT_TOKEN, WEBHOOK_URL, HOST, PORT
from handlers import handle_message, handle_callback

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)

async def webhook_handler(request: web.Request) -> web.Response:
    """Принимает входящие события от MAX и передаёт обработчикам"""
    try:
        update = await request.json()
        update_type = update.get('update_type')

        if update_type == UpdateType.MESSAGE_CREATED:
            from maxapi.types import Message
            message = Message(**update['message'])
            await handle_message(bot, message)

        elif update_type == UpdateType.MESSAGE_CALLBACK:
            from maxapi.types import CallbackQuery
            callback = CallbackQuery(**update['callback'])
            await handle_callback(bot, callback)

        return web.Response(status=200, text='OK')

    except Exception as e:
        logger.error(f'Ошибка обработки события: {e}')
        return web.Response(status=500)

async def on_startup(app: web.Application):
    """Регистрирует вебхук при старте сервера"""
    await bot.set_webhook(url=WEBHOOK_URL)
    logger.info(f'Вебхук зарегистрирован: {WEBHOOK_URL}')

async def main():
    app = web.Application()
    app.router.add_post('/webhook', webhook_handler)
    app.on_startup.append(on_startup)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, HOST, PORT)
    logger.info(f'Сервер запущен на {HOST}:{PORT}')
    await site.start()
    await asyncio.Event().wait()

if __name__ == '__main__':
    asyncio.run(main())