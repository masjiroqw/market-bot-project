from enum import Enum

from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class CurrencyType(Enum):
    ton = 'TON'
    usdt = 'USDT'


class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    
    
    
class Seller(Base):
    __tablename__ = 'sellers'
    
    seller_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    
    


class Product(Base):
    __tablename__ = 'products'
   
   
    id: Mapped[int] = mapped_column(primary_key=True)
    seller_id: Mapped[int] = mapped_column(ForeignKey('sellers.seller_id'))
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(2000))
    currency: Mapped[CurrencyType]
    price: Mapped[int]
    photo_id: Mapped[str| None]
    product_tg_id: Mapped[str]
    
    
    

    
    

    
    
    