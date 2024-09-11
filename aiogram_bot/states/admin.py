from aiogram.fsm.state import State, StatesGroup


class AdState(StatesGroup):
    content = State()


class Update_xls(StatesGroup):
    xls = State()