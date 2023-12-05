import asyncio
import logging
import psycopg_pool

from aiogram import Bot, Dispatcher
from aiogram.types import Message

from core.settings import settings
from core.handlers import start, reception, cancel_reception, all_reconrdings
from core.middlewares.database_middleware import UsersDatabaseMiddleware, ReceptionDatabaseMiddleware


def get_pool(host, dbname, user, password):
    return psycopg_pool.AsyncConnectionPool(f"host={host} port=5432 dbname={dbname} user={user} password={password} " f"connect_timeout=60")

async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(settings.bots.bot_token, parse_mode='HTML')
    dp = Dispatcher()
    pool = get_pool(settings.server.host, settings.server.db_name, settings.server.user, settings.server.password)

    dp.startup.register(start.bot_start)
    dp.include_router(start.router)
    dp.include_router(reception.router)
    dp.include_router(cancel_reception.router)
    dp.include_router(all_reconrdings.router)

    dp.update.middleware(UsersDatabaseMiddleware(pool))
    dp.update.middleware(ReceptionDatabaseMiddleware(pool))

    try:
        await dp.start_polling(bot)
    except:
        await bot.session.close()

if __name__=='__main__':
    asyncio.run(main())
