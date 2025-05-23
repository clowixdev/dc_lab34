import asyncio

from handlers import default, admin
from loader import bot, dp


async def main():
    dp.include_router(admin.router)
    dp.include_router(default.router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    print("Bot has been launched...")
    asyncio.run(main())