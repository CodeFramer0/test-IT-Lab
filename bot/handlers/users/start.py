from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.inline import cb_start_action, start_keyboard
from loader import dp
from utils.utils import delete_last_message, state_finish


def _build_start_text(user: dict) -> str:
    text = (
        f"Здравствуйте, {user.get('name', 'пользователь')}!\n\n"
        f"Я TODO бот, который поможет управлять Вашими задачами.\n"
        f'Чтобы посмотреть свои таски, воспользуйтесь кнопкой "Мои задачи", там же Вы сможете создать новую задачу!\n\n'
        "Как только срок выполнения задачи истечет, я сообщу Вам об этом."
    )
    return text


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message, user: dict, state: FSMContext):
    await message.answer(
        _build_start_text(user),
        reply_markup=start_keyboard(),
    )


@dp.callback_query_handler(cb_start_action.filter(action="start_menu"), state="*")
async def start_menu(query: types.CallbackQuery, user: dict, state: FSMContext):
    await query.answer()
    await state_finish(state)
    await delete_last_message(query.message)
    await query.message.answer(
        _build_start_text(user),
        reply_markup=start_keyboard(),
    )
