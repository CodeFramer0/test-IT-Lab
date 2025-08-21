import asyncio

from aiogram import Dispatcher, types
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled
from pydantic.types import Union


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit=DEFAULT_RATE_LIMIT, key_prefix="antiflood_"):
        self.rate_limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()

    async def throttle(self, target: Union[types.Message, types.CallbackQuery]):
        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()
        if not handler:
            return
        limit = getattr(handler, "throttling_rate_limit", self.rate_limit)
        key = getattr(handler, "throttling_key", f"{self.prefix}_{handler.__name__}")

        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled as t:
            await self.target_throttled(target, t, dispatcher, key)
            raise CancelHandler()

    @staticmethod
    async def target_throttled(
        target: Union[types.Message, types.CallbackQuery],
        throttled: Throttled,
        dispatcher: Dispatcher,
        key: str,
    ):
        message = target.message if isinstance(target, types.CallbackQuery) else target
        delta = throttled.rate - throttled.delta

        if throttled.exceeded_count == 2:
            if type(target) == types.Message:
                await message.answer(
                    f"Слишком много запросов, подождите: {round(delta, 3)} сек"
                )
            elif type(target) == types.CallbackQuery:
                await target.answer(
                    f"Слишком много запросов, подождите: {round(delta, 3)} сек"
                )
            await asyncio.sleep(delta)

            return

    async def on_process_message(self, message, data):
        await self.throttle(message)

    async def on_process_callback_query(self, call, data):
        await self.throttle(call)
