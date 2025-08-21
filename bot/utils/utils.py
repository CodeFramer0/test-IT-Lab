import logging

from aiogram.dispatcher import FSMContext
from dateutil import parser
from loader import bot


def format_datetime(dt_str: str | None, fmt: str = "%d.%m.%Y %H:%M") -> str:
    if not dt_str:
        return "—"
    try:
        dt = parser.isoparse(dt_str)
        return dt.strftime(fmt)
    except (ValueError, TypeError):
        return "—"


async def delete_message(chat_id, message_id):
    try:
        await bot.delete_message(chat_id, message_id)
    except Exception as e:
        logging.error(f"Не удалось удалить сообщение: {e}")


async def delete_last_message(message):
    try:
        await message.delete()
    except Exception as e:
        logging.error(f"Не удалось удалить последнее сообщение: {e}")


async def state_finish(state: FSMContext):
    try:
        await state.finish()
    except Exception as e:
        logging.error(f"Невозможно завершить состояние: {e}")
