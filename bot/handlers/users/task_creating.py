from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.inline import cancel_task_keyboard, cb_start_action
from keyboards.inline.category_keyboards import (category_keyboard,
                                                 cb_category_action)
from loader import category_api, dp, task_api
from states.tasks_state import AddTaskState
from utils.utils import delete_last_message, state_finish

from .tasks import task_menu_message


@dp.callback_query_handler(cb_start_action.filter(action="add_task"), state="*")
async def start_add_task(query: types.CallbackQuery, state: FSMContext):
    await query.answer()
    await state_finish(state)
    await delete_last_message(query.message)
    await query.message.answer(
        "Введите название задачи:", reply_markup=cancel_task_keyboard()
    )
    await AddTaskState.waiting_for_title.set()


@dp.message_handler(
    state=AddTaskState.waiting_for_title, content_types=types.ContentTypes.TEXT
)
async def process_task_title(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer(
        "Введите описание задачи:", reply_markup=cancel_task_keyboard()
    )
    await AddTaskState.waiting_for_description.set()


@dp.message_handler(
    state=AddTaskState.waiting_for_description, content_types=types.ContentTypes.TEXT
)
async def process_task_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text or "")
    categories = await category_api.get()
    categories = [categories] if isinstance(categories, dict) else categories
    if not categories:
        await message.answer("Нет доступных категорий. Пожалуйста, создайте категорию.")
        return
    await message.answer(
        "Выберите категорию задачи:", reply_markup=category_keyboard(categories)
    )
    await AddTaskState.waiting_for_category.set()


@dp.callback_query_handler(
    cb_category_action.filter(action="select_category"),
    state=AddTaskState.waiting_for_category,
)
async def process_task_category(
    query: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    category_id = callback_data.get("category_id")
    await state.update_data(category=category_id)
    await query.answer()
    await query.message.answer(
        "Введите срок выполнения задачи (формат: YYYY-MM-DD HH:MM America/Adak):",
        reply_markup=cancel_task_keyboard(),
    )
    await AddTaskState.waiting_for_due_date.set()


@dp.message_handler(
    state=AddTaskState.waiting_for_due_date, content_types=types.ContentTypes.TEXT
)
async def process_task_due_date(message: types.Message, state: FSMContext, user: dict):
    due_date_text = message.text.strip()
    due_date = None
    if due_date_text:
        try:
            due_date = datetime.strptime(due_date_text, "%Y-%m-%d %H:%M")
            due_date_iso = due_date.isoformat()
        except Exception:
            await message.answer(
                "Неверный формат даты. Попробуйте ещё раз:",
                reply_markup=cancel_task_keyboard(),
            )
            return

    data = await state.get_data()
    task_payload = {
        "title": data["title"],
        "description": data["description"],
        "category": data["category"],
        "telegram_user": user["id"],
        "due_date": due_date_iso,
    }
    task = await task_api.create(body=task_payload)

    if task is None:
        return
    await task_menu_message(message, user, state)
