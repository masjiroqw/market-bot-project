import asyncio

from database.database import Base, engine
from database.schema import Seller, User


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(create_tables())
