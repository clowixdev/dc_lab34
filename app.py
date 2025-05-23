import asyncio
from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from handlers import default, admin
from loader import bot, dp, TUNA, WEBHOOK_PATH, ADMIN_ID, HOST, PORT


async def on_startup() -> None:
    await bot.set_webhook(f"{TUNA}{WEBHOOK_PATH}")
    await bot.send_message(chat_id=ADMIN_ID, text="started!")


async def on_shutdown() -> None:
    await bot.send_message(chat_id=ADMIN_ID, text="shuted down...")
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.session.close()


async def main():
    dp.include_router(admin.router)
    dp.include_router(default.router)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    app = web.Application()

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot
    )

    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)
    await web._run_app(app, host=HOST, port=PORT)


if __name__ == "__main__":
    asyncio.run(main())