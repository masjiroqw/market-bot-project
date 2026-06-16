
import logging

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.database import session
from database.repositories import ProductRepo, SellerRepo
from FSM.fsm_states import CreateProduct
from keyboards import become_a_seller_kb, main_kb, seller_dashboard, set_currency
from logger_config import setup_logger
from service import Seller_

logger = logging.getLogger('market_bot')
main_router = Router()


#Теперь main видит данный роутер и подхватывает декораторы из этого файла
@main_router.message(Command("start"))
async def comand_start_handler(message:Message):
    args = message.text.split()
    if len(args) > 1 and args[1].startswith('product_'):
        new_args = args[1].split('_')
        try:
            product_id = int(new_args[1])
            async with session() as s:
              repo = ProductRepo(s)
              product = await repo.show_product(product_id)
              if product.photo_id is not None:
                  caption = f'Название товара: {product.name}\n Описание товара: {product.description}\n Цена {product.price} в {product.currency.value}'
                  await message.answer_photo(photo=product.photo_id, caption=caption)
                  return
              else:
                  await message.answer(f'Название товара: {product.name}\n Описание товара: {product.description}\n Цена {product.price} в {product.currency.value}')
                  return 
        except TypeError as t:
            logger.info(f'Ошибка {t}')
    username = message.from_user.first_name if message.from_user else 'Гость'
    #Почему не просто first_name? Потому что у нас message.from_user.first_name может быть пустым,
    await message.answer(f'Привет {username}, выбери раздел:', reply_markup=main_kb)

        
    
    
    
    
@main_router.callback_query(F.data == 'seller')
async def handler_seller_button(callback:CallbackQuery):
        try:
            async with session() as s:
                db = SellerRepo(s)
                seller = await db.find_seller()
       
            
            if seller:
                await callback.message.edit_text(text = 'Ваш личный кабинет 💼', reply_markup=seller_dashboard )
            
            else:
                username = callback.message.chat.first_name if callback.message.chat.first_name else 'Гость'
                seller = Seller_(f'{username}')
                text_from_service = await seller.say_hi_seller()
                final_text = f'{text_from_service}\n Тогда жми кнопку ниже!💎'
                await callback.answer()
                await callback.message.edit_text(text = final_text, reply_markup=become_a_seller_kb) 
        except ConnectionError  as c:
            logger.error(f'{c}') 
    
@main_router.callback_query(F.data == 'dashboard')
async def dashboard(callback:CallbackQuery):
    async with session() as s:
        db = SellerRepo(s)
        await db.create_seller(callback.from_user.id)
    await callback.answer()
    await callback.message.edit_text(text = 'Ваш личный кабинет 💼', reply_markup=seller_dashboard ) 
    

        
    
    





