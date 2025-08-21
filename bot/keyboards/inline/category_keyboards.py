from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from .start_keyboards import cb_start_action

cb_category_action = CallbackData("category", "action", "category_id")


def category_keyboard(categories: list[dict]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)

    for category in categories:
        keyboard.add(
            InlineKeyboardButton(
                text=category["name"],
                callback_data=cb_category_action.new(
                    action="select_category", category_id=str(category["id"])
                ),
            )
        )
    keyboard.add(
        InlineKeyboardButton(
            text="Отмена",
            callback_data=cb_start_action.new(action="task_menu"),
        )
    )

    return keyboard
