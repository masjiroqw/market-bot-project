

import asyncio
import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

load_dotenv()

class Base(DeclarativeBase):
    pass

async_engine = create_async_engine(os.environ['DB_CONN'], pool_pre_ping=True)



session = async_sessionmaker(async_engine, expire_on_commit=False, class_= AsyncSession)




