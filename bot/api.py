import logging

import aiohttp
from config import API_URL

# HEADERS = {"Authorization": f"token {API_TOKEN}", "Accept": "application/json"}
HEADERS = {"Accept": "application/json"}


class BaseAPI:
    """Базовый клиент для работы с REST API."""

    def __init__(self, endpoint: str):
        self.api_url = f"{API_URL}{endpoint}/"

    @staticmethod
    async def _process_response(response: aiohttp.ClientResponse) -> dict | None:
        try:
            data = await response.json()
            response.raise_for_status()
            if isinstance(data, list):
                data = data if len(data) > 1 else data[0] if data else None
            return data
        except (aiohttp.ClientError, ValueError) as e:
            logging.error(f"Ошибка обработки ответа: {e}")
            logging.error(f"Статус: {response.status}")
            logging.error(f"Тело ответа: {await response.text()}")
            return None

    async def create(
        self,
        body: dict | None = None,
        form: aiohttp.FormData | None = None,
    ) -> dict | None:
        async with aiohttp.ClientSession() as session:
            try:
                if form:
                    async with session.post(
                        self.api_url, data=form, headers=HEADERS
                    ) as resp:
                        return await self._process_response(resp)
                else:
                    async with session.post(
                        self.api_url, json=body, headers=HEADERS
                    ) as resp:
                        return await self._process_response(resp)
            except aiohttp.ClientError as e:
                logging.error(f"POST: {e} | URL: {self.api_url}")
            return None

    async def get(
        self, id: int | None = None, params: dict | None = None
    ) -> dict | None:
        url = f"{self.api_url}{id}/" if id else self.api_url
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, params=params, headers=HEADERS) as resp:
                    return await self._process_response(resp)
            except aiohttp.ClientError as e:
                logging.error(f"GET: {e} | URL: {url}")
        return None

    async def update(self, id: int, body: dict | None = None) -> dict | None:
        url = f"{self.api_url}{id}/"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.put(url, json=body, headers=HEADERS) as resp:
                    return await self._process_response(resp)
            except aiohttp.ClientError as e:
                logging.error(f"PUT: {e} | URL: {url}")
        return None

    async def delete(self, id: int) -> bool:
        url = f"{self.api_url}{id}/"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.delete(url, headers=HEADERS) as resp:
                    if resp.status == 204:
                        return True
                    logging.error(f"DELETE: неверный статус {resp.status}")
            except aiohttp.ClientError as e:
                logging.error(f"DELETE: {e} | URL: {url}")
        return False


class TelegramUserAPI(BaseAPI):
    def __init__(self):
        super().__init__("telegram-users")


class CategoryAPI(BaseAPI):
    def __init__(self):
        super().__init__("categories")


class TaskAPI(BaseAPI):
    def __init__(self):
        super().__init__("tasks")

    async def mark_completed(self, task_id: str) -> dict | None:
        url = f"{self.api_url}{task_id}/mark_completed/"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, headers=HEADERS) as resp:
                    return await self._process_response(resp)
            except aiohttp.ClientError as e:
                logging.error(f"POST mark_completed: {e} | URL: {url}")
        return None

    async def mark_incomplete(self, task_id: str) -> dict | None:
        url = f"{self.api_url}{task_id}/mark_incomplete/"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, headers=HEADERS) as resp:
                    return await self._process_response(resp)
            except aiohttp.ClientError as e:
                logging.error(f"POST mark_incomplete: {e} | URL: {url}")
        return None
