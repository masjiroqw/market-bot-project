

from aiogram.fsm.state import State, StatesGroup


class CreateProduct(StatesGroup):
    product_tg_id = State()
    product_name = State()
    description = State()
    price = State()
    currency = State()
    photo = State()
    skip_step = State()
    