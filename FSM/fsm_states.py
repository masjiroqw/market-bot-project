

from aiogram.fsm.state import State, StatesGroup


class CreateProduct(StatesGroup):
    product_name = State()
    description = State()
    price = State()
    currency = State()
    photo = State()
    