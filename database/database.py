from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv
import os


load_dotenv()

class Base(DeclarativeBase):
    pass

engine = create_async_engine(os.environ['DB_CONN'])


session = async_sessionmaker(engine, expire_on_commit=False, class_= AsyncSession)




