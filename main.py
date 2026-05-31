import os, aiogram, asyncio, logging
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from logger_config import setup_logger
from handlers import router





load_dotenv()
logger = setup_logger()
logging.basicConfig(level=logging.INFO)



bot = Bot(token=os.environ['BOT_TOKEN'])
dp = Dispatcher()
dp.include_router(router)





async def main():
    try:
        logger.info('Пробуем запустить бота')
        logging.INFO
        await dp.start_polling(bot)
        
        
    except Exception as e:
        logger.error(f'Ошибка : {e}')
        
        
asyncio.run(main())
    



