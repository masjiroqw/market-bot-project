
import logging

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.database import session
from database.repositories import SellerRepo
from FSM.fsm_states import CreateProduct
from keyboards import become_a_seller_kb, main_kb, seller_dashboard, set_currency
from logger_config import setup_logger
from service import Seller_

logger = logging.getLogger('market_bot')
main_router = Router()


#Теперь main видит данный роутер и подхватывает декораторы из этого файла
@main_router.message(CommandStart())
async def comand_start_handler(message:Message):

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
    

        
    
    





