import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from config import API_TOKEN, REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWORD

from db import create_pool
from db import create_table

# Настройка логирования
logging.basicConfig(level=logging.INFO)


# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
# storage = MemoryStorage()
storage = RedisStorage2(
    host=REDIS_HOST, 
    port=REDIS_PORT,
    db=REDIS_DB,
    password=REDIS_PASSWORD,
    
)
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())


async def on_startup(dp):
    dp["db_pool"] = await create_pool()
    async with dp["db_pool"].acquire() as conn:
        await create_table(conn)


if __name__ == "__main__":
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
