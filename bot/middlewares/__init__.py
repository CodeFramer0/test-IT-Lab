from loader import dp, storage

from .throttling import ThrottlingMiddleware
from .user_exists import UserExistsMiddleware

if __name__ == "middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(UserExistsMiddleware(storage, user_ttl_days=180))
