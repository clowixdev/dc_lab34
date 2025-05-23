import asyncio
from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from handlers import default, admin
from loader import bot, dp


async def main():
    dp.include_router(admin.router)
    dp.include_router(default.router)

    await bot.set_webhook("https://clowixdev.pythonanywhere.com/post")
    # await dp.start_polling(bot)

    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )
    webhook_requests_handler.register(app, path="/post")
    setup_application(app, dp, bot=bot)
    await web._run_app(app, host="127.0.0.1", port=8443)

if __name__ == "__main__":
    print("Bot has been launched...")
    asyncio.run(main())