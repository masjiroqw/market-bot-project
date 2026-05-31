
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



main_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Продавец 💼', callback_data='seller')],
    [InlineKeyboardButton(text='Покупатель 💰', callback_data='buyer')]
    
])

become_a_seller_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = 'Стать продавцом✅', callback_data='dashboard')]
])


seller_dashboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = 'Создать товар 🔑', callback_data='create_product')],
    [InlineKeyboardButton(text = 'Баланс 💰', callback_data='balance')]
])