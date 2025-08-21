from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from keyboards.inline.start_keyboards import cb_start_action

cb_task_action = CallbackData("task", "action", "task_id", "status")


def task_keyboard(tasks: list[dict]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    if tasks:
        for idx, task in enumerate(tasks, start=1):
            if task.get("is_expired"):
                status_emoji = "⏰"
                status_flag = "expired"
            elif task.get("is_completed"):
                status_emoji = "✅"
                status_flag = "completed"
            else:
                status_emoji = "❌"
                status_flag = "pending"

            btn_text = f"{idx}. {status_emoji} {task['title']}"

            keyboard.add(
                InlineKeyboardButton(
                    text=btn_text,
                    callback_data=cb_task_action.new(
                        action="task_switch_status",
                        task_id=task["id"],
                        status=status_flag,
                    ),
                )
            )
    keyboard.add(
        InlineKeyboardButton(
            text="Отобразить по категории 🗂️",
            callback_data=cb_start_action.new(action="sort_by_category"),
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text="Создать задачу ➕",
            callback_data=cb_start_action.new(action="add_task"),
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text="Начальное меню",
            callback_data=cb_start_action.new(action="start_menu"),
        )
    )
    return keyboard


def cancel_task_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(
            text="Отмена",
            callback_data=cb_start_action.new(action="task_menu"),
        )
    )
    return keyboard
