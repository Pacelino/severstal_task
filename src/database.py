from fastapi import Depends, HTTPException

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlmodel import SQLModel


""" 
Создание engine и хранения session
"""

sqlite_file_name = "roll.db"
engine = create_async_engine(f"sqlite+aiosqlite:///{sqlite_file_name}")
# new_session = async_sessionmaker(engine)


async def get_session():
    async with AsyncSession(engine) as session:
        yield session
        



async def setup_table():
    try:
        async with engine.begin() as conn:
            # await conn.run_sync(SQLModel.metadata.drop_all)
            await conn.run_sync(SQLModel.metadata.create_all)
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=404, detail="Failed create database")
    
