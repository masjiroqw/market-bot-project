import logging
from collections.abc import Awaitable, Callable
from mailbox import Message
from typing import Any, Callable
from xml.sax import handler

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, TelegramObject
from sqlalchemy import event
from sqlalchemy.ext.asyncio import async_sessionmaker

from database.repositories import UserRepo
from logger_config import setup_logger

logger = logging.getLogger('market_bot')

class RegistrationMiddleware(BaseMiddleware):
    def __init__(self, session: async_sessionmaker) -> None:
        self.session = session
        
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        
        if isinstance(event, CallbackQuery|Message):
            logger.info('Прилетел колбэк')
            async with self.session() as s:
             repo = UserRepo(s)
             user = await repo.create_user(event.from_user.id) 
             data['user'] = user
             logger.info('И до сюда я тоже дошел')
             return await handler(event, data) 
        return await handler(event, data)
        

