from aiogram.fsm.state import State, StatesGroup


class Guardianship(StatesGroup):
    number = State()

class PaymentHistoryParent(StatesGroup):
    select_child = State()
    select_payment = State()
    selected_year = State()
