from aiogram.dispatcher.middlewares import BaseMiddleware
from api import TelegramUserAPI


class UserExistsMiddleware(BaseMiddleware):
    def __init__(self, storage, user_ttl_days: int | None = None):
        super().__init__()
        self.api = TelegramUserAPI()
        self.redis = storage.redis
        self.user_ttl_seconds = user_ttl_days * 86400 if user_ttl_days else None

    async def _get_or_create_or_update(self, tg_user):
        user_id = tg_user.id
        nick_name = tg_user.username or "NoName"

        user = await self.api.get(params={"user_id": user_id})

        if not user:
            return await self.api.create(
                body={
                    "name": tg_user.full_name,
                    "nick_name": nick_name,
                    "user_id": user_id,
                }
            )

        if user["name"] != tg_user.full_name or user["nick_name"] != nick_name:
            return await self.api.update(
                id=user["id"],
                body={
                    "user_id": user_id,
                    "name": tg_user.full_name,
                    "nick_name": nick_name,
                },
            )

        return user

    async def on_pre_process_message(self, message, data: dict):
        data["user"] = await self._get_or_create_or_update(message.from_user)

    async def on_pre_process_callback_query(self, callback_query, data: dict):
        data["user"] = await self._get_or_create_or_update(callback_query.from_user)
