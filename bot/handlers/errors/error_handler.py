import logging

from aiogram.utils.exceptions import (CantDemoteChatCreator, CantParseEntities,
                                      InvalidQueryID, MessageCantBeDeleted,
                                      MessageNotModified, MessageTextIsEmpty,
                                      MessageToDeleteNotFound, RetryAfter,
                                      TelegramAPIError, Unauthorized)
from loader import dp


@dp.errors_handler()
async def errors_handler(update, exception):
    """
    Глобальный обработчик ошибок телеграм-бота.
    Ловим стандартные исключения aiogram и логируем их,
    чтобы не падало все приложение.
    """

    if isinstance(exception, CantDemoteChatCreator):
        logging.exception("Невозможно понизить создателя чата")
        return True

    if isinstance(exception, MessageNotModified):
        logging.exception("Сообщение не изменилось (MessageNotModified)")
        return True

    if isinstance(exception, MessageCantBeDeleted):
        logging.exception("Сообщение нельзя удалить")
        return True

    if isinstance(exception, MessageToDeleteNotFound):
        logging.exception("Сообщение для удаления не найдено")
        return True

    if isinstance(exception, MessageTextIsEmpty):
        logging.exception("Пустой текст сообщения")
        return True

    if isinstance(exception, Unauthorized):
        logging.exception(f"Ошибка авторизации: {exception}")
        return True

    if isinstance(exception, InvalidQueryID):
        logging.exception(f"Неверный query_id: {exception} \nUpdate: {update}")
        return True

    if isinstance(exception, TelegramAPIError):
        logging.exception(f"Ошибка Telegram API: {exception} \nUpdate: {update}")
        return True

    if isinstance(exception, RetryAfter):
        logging.exception(f"Превышен лимит запросов.{exception} \nUpdate: {update}")
        return True

    if isinstance(exception, CantParseEntities):
        logging.exception(f"Ошибка парсинга entities: {exception} \nUpdate: {update}")
        return True

    logging.exception(
        f"Необработанная ошибка\nUpdate: {update}\nException: {exception}"
    )
