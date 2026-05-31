import aiogram
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command, CommandStart
from service import Seller_
from keyboards import main_kb, become_a_seller_kb, seller_dashboard
from main import setup_logger
from .database.database import session
from database.repositories import UserRepo, SellerRepo


logger = setup_logger()


#Регаем роутер 
router = Router()




#Теперь main видит данный роутер и подхватывает декораторы из этого файла
@router.message(CommandStart())
async def comand_start_handler(message:Message):
   
    async with session() as s:
        db = UserRepo(s)
        user = await db.create_user(message.from_user.id)
     
    
    username = message.from_user.first_name if message.from_user else 'Гость'
    logger.info(f'Создаем айди пользователяю{message.from_user.first_name}')
    #Почему не просто first_name? Потому что у нас message.from_user.first_name может быть пустым,
    await message.answer(f'Привет {username}, выбери раздел:', reply_markup=main_kb)

        
    
    
    
    
@router.callback_query(F.data == 'seller')
async def handler_seller_button(callback:CallbackQuery):

            async with session() as s:
                db = SellerRepo(s)
                seller = db.find_seller(callback.from_user.id)
            if seller:
                await callback.message.edit_text(text = 'Ваш личный кабинет 💼', reply_markup=seller_dashboard )
            
            else:
                username = callback.message.chat.first_name if callback.message.chat.first_name else 'Гость'
                seller = Seller_(f'{username}')
                text_from_service = await seller.say_hi_seller()
                final_text = f'{text_from_service}\n Тогда жми кнопку ниже!💎'
                await callback.answer()
                await callback.message.edit_text(text = final_text, reply_markup=become_a_seller_kb) 
            
    
@router.callback_query(F.data == 'dashboard')
async def dashboard(callback:CallbackQuery):
    async with session() as s:
        db = SellerRepo(s)
        await db.create_seller(callback.from_user.id)
    await callback.answer()
    await callback.message.edit_text(text = 'Ваш личный кабинет 💼', reply_markup=seller_dashboard ) 
    
    
    
    
    
        
    
    





