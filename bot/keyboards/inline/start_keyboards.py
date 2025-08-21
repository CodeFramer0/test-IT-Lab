from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

cb_start_action = CallbackData("start", "action")


def start_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.insert(
        InlineKeyboardButton(
            text="Мои задачи",
            callback_data=cb_start_action.new(action="task_menu"),
        ),
    )

    return keyboard


def back_to_menu_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(
            text="Вернуться в меню",
            callback_data=cb_start_action.new(action="main_menu"),
        )
    )
    return keyboard
