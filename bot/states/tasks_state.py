from aiogram.dispatcher.filters.state import State, StatesGroup


class AddTaskState(StatesGroup):
    waiting_for_title = State()
    waiting_for_description = State()
    waiting_for_category = State()
    waiting_for_due_date = State()
