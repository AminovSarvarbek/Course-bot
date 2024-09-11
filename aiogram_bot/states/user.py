from aiogram.fsm.state import StatesGroup, State


class UserRegisterState(StatesGroup):
    name = State()
    phone = State()
    school = State()
    class_ = State()
    direction = State()


