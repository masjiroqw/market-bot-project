import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

import FSM.fsm_states
import handlers.fsmhandlers
import handlers.mainhandlers
from database.database import session
from handlers.fsmhandlers import fsm_router
from handlers.mainhandlers import main_router
from logger_config import setup_logger
from middleware import RegistrationMiddleware

load_dotenv()
logger = setup_logger()
logging.basicConfig(level=logging.INFO)





bot = Bot(token=os.environ['BOT_TOKEN'])
dp = Dispatcher()
dp.include_router(main_router)
dp.include_router(fsm_router)

dp.callback_query.middleware(RegistrationMiddleware(session=session))




async def main():
    try:
        logger.info('Пробуем запустить бота')
        logging.INFO
        await dp.start_polling(bot)
        
        
    except Exception as e:
        logger.error(f'Ошибка : {e}')
        
        
asyncio.run(main())
    



