from sqlalchemy.orm import Mapped, mapped_column
from .database import Base
from sqlalchemy import BigInteger, ForeignKey, String
import enum 


class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    
    
    
class Seller(Base):
    __tablename__ = 'sellers'
    
    seller_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    
    
    
    
    

    
    

    
    
    