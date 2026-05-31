from venv import logger

from .schema import User, Seller
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select, select


class UserRepo:
    #инициализируем сессию, чтобы у нас для каждого была своя отдельная сессия
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
    #метод  создания юзера в бд    
    async def create_user(self, tg_id:int):
        user = select(User).where(User.tg_id == tg_id)
        result = await self.session.execute(user)
        obj = result.scalar_one_or_none()
        
        if obj is None:
            new_user = User(tg_id = tg_id)
            self.session.add(new_user)
            await self.session.commit()
            await self.session.refresh(new_user)  
            logger.info('Пользователь зарегистрирован')  
            return new_user
        logger.info('Пользователь найден')
        return obj
        
    
class SellerRepo(UserRepo):
    def __init__(self, session:AsyncSession) -> None:
        self.session = session
        
    async def find_seller(self, tg_id:int):
        seller = select(Seller).where(User.tg_id == tg_id)
        result = await self.session.execute(seller)
        seller_obj = result.scalar_one_or_none()
        logger.info('Продавец найден')
        return seller_obj
    logger.info('Продавец не найден')
    
    #Сам написал!! Трудно конечно связи было продумать, но зато все из своей идеи!
    #Функуия создания продавца, для его создания вызывается метод create_user
    #Который в свою очередь в любом случае вернет нам объект юзера в котором уже лежит айди
    #Далее исходя из структуры схемы, мы приравниваем айди который лежит в result(то есть айди юзера) айди селлера

    async def create_seller(self, tg_id:int):
        result = await self.create_user(tg_id)
        new_seller = Seller(seller_id = result.id)
        self.session.add(new_seller)
        await self.session.commit()
        await self.session.refresh(new_seller)
        logger.info('Продавец зарегистрирован')
        return new_seller


    
        


