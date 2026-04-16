from fastapi import FastAPI, HTTPException, Depends, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.database.engine import Session
from core.database.models import User

async def get_db():
    async with Session() as session:
        yield session

async def get_current_user(api_key: str = Header(None), db: AsyncSession = Depends(get_db)):
    if not api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='В headers отсустствует API KEY')
    result = await db.execute(select(User).where(User.api_key == api_key))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='API KEY не найден')
    return user