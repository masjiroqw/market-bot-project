

import logging
from ast import Call

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.database import session
from database.repositories import ProductRepo, SellerRepo
from database.schema import Product
from FSM.fsm_states import CreateProduct
from keyboards import set_currency, skip_step

logger = logging.getLogger('market_bot')

fsm_router = Router()

#Ловим колбэк на создание товара, и выбираем состояние
@fsm_router.callback_query(F.data == 'create_product')
async def create_product_button(callback:CallbackQuery, state:FSMContext):
    logger.info('Вижу колбэк на создание товара')
    
    await callback.answer()
    await state.set_state(CreateProduct.product_tg_id)
    await callback.message.answer('Пришлите товар')
    
    

@fsm_router.message(CreateProduct.product_tg_id)
async def process_file_id(message:Message, state:FSMContext):
    if message.text:
        await state.update_data(product = message.text)
    elif message.document:
        await state.update_data(product = message.document.file_id)
    elif message.photo:
        await state.update_data(product = message.photo[-1].file_id)
    await state.set_state(CreateProduct.product_name)
    await message.answer('Пришлите название товара')
    
   
        
    


    
    
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
    await callback.answer()
    await state.update_data(currency = callback.data)
    await state.set_state(CreateProduct.price)
    logger.info('USDT обработчик заюзан')
    await callback.message.answer('Введите цену товара')
    
@fsm_router.callback_query(CreateProduct.currency, F.data == 'ton')
async def process_currency_ton(callback:CallbackQuery, state:FSMContext):
    await callback.answer()
    await state.update_data(currency = callback.data)
    await state.set_state(CreateProduct.price)
    logger.info('TON обработичк заюзался')
    await callback.message.answer('Введите цену товара')

    
    
    
@fsm_router.message(CreateProduct.price)
async def process_price(message:Message, state:FSMContext):
    try:
    
    
        await state.update_data(price = int(message.text))
        await state.set_state(CreateProduct.photo)
        await message.answer('Пришлите фотографию товара \n или карточку товара', reply_markup=skip_step)
    except ValueError:
        message.answer('Пожалуйста, введите число')


        
@fsm_router.message(CreateProduct.photo, F.photo)
async def process_photo(message:Message, state:FSMContext):
    
    photo_id = message.photo[-1].file_id
    await state.update_data(photo = photo_id)
    data = await state.get_data()
    product_tg_id = data.get('product', 0)
    product_name = data.get('item_name', 0)
    description = data.get('description', 0)
    value = data.get('currency', 0)
    price = data.get('price', 0)
    photo = data.get('photo', 0)
    
    async with session() as s:
        product_repo = ProductRepo(s)
        seller_repo = SellerRepo(s)
        obj = await seller_repo.find_seller()
        
        get_id = await product_repo.save_data(seller_id = obj , 
                             product_tg_id=product_tg_id,
                             product_name=product_name, 
                             description=description, 
                             currency=value, 
                             price=price, 
                             photo_id=photo)
        product_id = get_id.id
        product_link = f'https://t.me/HashPagebot?start=product_{product_id}'
        caption = (f'Название товара: {product_name}\n Описание товара: {description}\n Цена: {price} в {value}\n Ссылка на товар: {product_link}')
        await message.answer_photo(photo=photo, caption=caption)  
        await state.clear()
        

@fsm_router.callback_query(F.data == 'skip')
async def skip_photo(callback:CallbackQuery, state:FSMContext):
    await callback.answer()
    data = await state.get_data()
    product_tg_id = data.get('product', 0)
    product_name = data.get('item_name', 0)
    description = data.get('description', 0)
    value = data.get('currency', 0)
    price = data.get('price', 0)
    photo = None
    async with session() as s:
        product_repo = ProductRepo(s)
        seller_repo = SellerRepo(s)
        obj = await seller_repo.find_seller()
        
        get_id = await product_repo.save_data(seller_id = obj ,
                             product_tg_id=product_tg_id,
                             product_name=product_name, 
                             description=description, 
                             currency=value, 
                             price=price, 
                             photo_id = photo )
        product_id = get_id.id
        product_link = f'https://t.me/HashPagebot?start=product_{product_id}'
    await state.set_state(CreateProduct.skip_step)
    caption = (f'Название товара: {product_name}\n Описание товара: {description}\n Цена: {price} в {value}\n Ссылка на товар: {product_link}')
    await callback.message.answer(caption)

    
    
    
    




