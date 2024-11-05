from sqlalchemy.orm import sessionmaker, scoped_session

import config

from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession

# Создание движка подключения к базе данных
engine = create_async_engine(config.DB_URL)
async_session = async_sessionmaker(engine, class_=AsyncSession)

def connection(func):
    '''
    Декоратор, который передает функции сессию как параметр
    '''
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            return await func(session, *args, **kwargs)

    return wrapper
