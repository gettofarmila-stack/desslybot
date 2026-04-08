import logging
from sqlalchemy import select
from database.models import User
from database.engine import Session


async def is_register(uid):
    async with Session() as session:
        user_obj = await session.execute(select(User).where(User.user_id == uid))
        user = user_obj.scalar_one_or_none()
        return(user)
    
async def registrate_user(uid, referrer_id):
    async with Session() as session:
        async with session.begin():
            new_user = User(user_id=uid, referrer_id=referrer_id)
            session.add(new_user)
        