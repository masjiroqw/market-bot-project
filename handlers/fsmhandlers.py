

import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.database import session
from database.repositories import ProductRepo, SellerRepo
from database.schema import Product
from FSM.fsm_states import CreateProduct
from keyboards import set_currency

logger = logging.getLogger('market_bot')

fsm_router = Router()


@fsm_router.callback_query(F.data == 'create_product')
async def create_product_button(callback:CallbackQuery, state:FSMContext):
    logger.info('Вижу колбэк на создание товара')
    await state.set_state(CreateProduct.product_name)
    await callback.message.answer('Введите название товара')
    await callback.answer()

    
    
@fsm_router.message(CreateProduct.product_name)
async def process_name(message:Message, state: FSMContext):
    await state.update_data(item_name = message.text)
    await state.set_state(CreateProduct.description)
    await message.answer('Введите описание товара')
    

@fsm_router.message(CreateProduct.description)
async def process_discroption(message:Message, state:FSMContext):
    await state.update_data(description = message.text)
    await state.set_state(CreateProduct.currency)
    await message.answer('Выберите валюту', reply_markup=set_currency)
    
    
@fsm_router.callback_query(CreateProduct.currency, F.data == 'usdt')
async def process_currency_usdt(callback:CallbackQuery, state:FSMContext):
    callback.answer()
    await state.update_data(currency = callback.data)
    await state.set_state(CreateProduct.price)
    logger.info('USDT обработчик заюзан')
    await callback.message.answer('Введите цену товара')
    
@fsm_router.callback_query(CreateProduct.currency, F.data == 'ton')
async def process_currency_ton(callback:CallbackQuery, state:FSMContext):
    callback.answer()
    await state.update_data(currency = callback.data)
    await state.set_state(CreateProduct.price)
    logger.info('TON обработичк заюзался')
    await callback.message.answer('Введите цену товара')

    
    
    
@fsm_router.message(CreateProduct.price)
async def process_price(message:Message, state:FSMContext):
    try:
    
    
        await state.update_data(price = int(message.text))
        await state.set_state(CreateProduct.photo)
        await message.answer('Пришлите фотографию товара \n или карточку товара')
    except ValueError:
        message.answer('Пожалуйста, введите число')


        
@fsm_router.message(CreateProduct.photo, F.photo)
async def process_photo(message:Message, state:FSMContext):
  
    photo_id = message.photo[-1].file_id
    await state.update_data(photo = photo_id)
    data = await state.get_data()
    product_name = data.get('item_name', 0)
    description = data.get('description', 0)
    value = data.get('currency', 0)
    price = data.get('price', 0)
    photo = data.get('photo', 0)
    async with session() as s:
        product_repo = ProductRepo(s)
        seller_repo = SellerRepo(s)
        obj = await seller_repo.find_seller()
        
        await product_repo.save_data(seller_id = obj ,product_name=product_name, 
                             description=description, 
                             currency=value, 
                             price=price, 
                             photo_id=photo)
        await state.clear()  




