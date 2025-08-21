from aiogram import executor
from handlers import *
from loader import dp, storage
from middlewares import *
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    await set_default_commands(dispatcher)


executor.start_polling(dp, skip_updates=False, on_startup=on_startup)
