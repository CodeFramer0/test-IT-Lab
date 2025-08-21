from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.inline import (category_keyboard, cb_category_action,
                              cb_start_action, cb_task_action, task_keyboard)
from loader import category_api, dp, task_api
from utils.utils import delete_last_message, format_datetime, state_finish


def _build_task_text(tasks: list[dict] | None) -> str:
    if not tasks:
        return (
            "☑️ На данный момент у Вас нет задач.\n\n"
            'Чтобы создать задачу, нажмите на кнопку "Создать задачу".'
        )
    text = "📋 <b>Ваши текущие задачи:</b>\n\n"
    task_text = ""
    for idx, task in enumerate(tasks, start=1):

        title = task.get("title")
        description = task.get("description", "—")
        category = task.get("category_name", "—")
        created_at = format_datetime(task.get("created_at"))
        due_date = format_datetime(task.get("due_date"))

        if task.get("is_completed"):
            title = f"<s>{title}</s> (Выполнено)"
        elif task.get("is_expired"):
            title = f"<s>{title}</s> (Истёк срок выполнения)"

        task_text += (
            f"📝 <strong>{idx}. {title}</strong>.\n"
            f"   🗒 Описание: {description}.\n"
            f"   🏷 Категория: <em>{category}.</em>\n"
            f"   🕒 Дата создания: <em>{created_at}.</em>\n"
            f"   ⏳ Срок выполнения: <em>{due_date}.</em> (America/Adak)\n"
            "────────────────────────────\n"
        )
    text = (
        f"{text}"
        f"{task_text}\n"
        "При нажатии на задачу, она автоматически переключает текущий статус.\n\n"
        "✅ - Задача выполнена.\n"
        "❌ - Задача не выполнена.\n"
        "⏰ - Задача просрочена.\n"
    )
    return text


@dp.callback_query_handler(cb_start_action.filter(action="task_menu"), state="*")
async def task_menu(query: types.CallbackQuery, user: dict, state: FSMContext):
    await query.answer()
    await state_finish(state)
    await delete_last_message(query.message)
    tasks = await task_api.get(params={"user_id": user["user_id"]})
    tasks = [tasks] if isinstance(tasks, dict) else tasks
    text = _build_task_text(tasks)
    await query.message.answer(text, reply_markup=task_keyboard(tasks))


async def task_menu_message(message: types.Message, user: dict, state: FSMContext):
    await state_finish(state)
    await delete_last_message(message)
    tasks = await task_api.get(params={"user_id": user["user_id"]})
    tasks = [tasks] if isinstance(tasks, dict) else tasks
    text = _build_task_text(tasks)
    await message.answer(text, reply_markup=task_keyboard(tasks))


@dp.callback_query_handler(
    cb_task_action.filter(action="task_switch_status"), state="*"
)
async def task_switch_status(
    query: types.CallbackQuery, user: dict, callback_data: dict, state: FSMContext
):
    await query.answer()

    task_id = callback_data["task_id"]
    current_status = callback_data["status"]

    if current_status == "expired":
        await query.answer("Эту задачу нельзя изменить ⏰", show_alert=True)
        return

    if current_status == "pending":
        task = await task_api.mark_completed(task_id)
    else:
        task = await task_api.mark_incomplete(task_id)

    if not task:
        await query.answer("Ошибка при обновлении задачи ❌", show_alert=True)
        return

    await task_menu(query, user, state)


@dp.callback_query_handler(cb_start_action.filter(action="sort_by_category"))
async def task_sort_by_category(
    query: types.CallbackQuery,
):
    await query.answer()
    await delete_last_message(query.message)
    categories = await category_api.get()
    categories = [categories] if isinstance(categories, dict) else categories
    if not categories:
        await query.message.answer(
            "Нет доступных категорий. Пожалуйста, создайте категорию."
        )
        return
    await query.message.answer(
        "Выберите категорию:", reply_markup=category_keyboard(categories)
    )


@dp.callback_query_handler(cb_category_action.filter(action="select_category"))
async def task_show_by_category(
    query: types.CallbackQuery,
    user: dict,
    callback_data: dict,
):
    await query.answer()
    await delete_last_message(query.message)
    tasks = await task_api.get(
        params={"user_id": user["user_id"], "category": callback_data["category_id"]}
    )
    tasks = [tasks] if isinstance(tasks, dict) else tasks
    text = _build_task_text(tasks)
    await query.message.answer(text, reply_markup=task_keyboard(tasks))
