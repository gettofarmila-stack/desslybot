import logging
from sqlalchemy import select
from database.models import User
from database.engine import Session
from utils.exceptions import DontHaveFunds, UserNotRegister
from decimal import Decimal


async def is_register(uid):
    async with Session() as session:
        user_obj = await session.execute(select(User).where(User.user_id == uid))
        user = user_obj.scalar_one_or_none()
        return(user)
    
async def registrate_user(uid, referrer_id):
    async with Session() as session:
        async with session.begin():
            if referrer_id is None:
                referrer_id = 0
            new_user = User(user_id=uid, referrer_id=int(referrer_id))
            session.add(new_user)
        
async def get_user_object(uid):
    async with Session() as session:
        user_obj = await session.execute(select(User).where(User.user_id == int(uid)))
        user = user_obj.scalar_one_or_none()
        return user
    
async def get_user_referrals(uid):
    async with Session() as session:
        ref_obj = await session.execute(select(User).where(User.referrer_id == int(uid)))
        ref_list = ref_obj.scalars().all()
        counter = 0
        for ref in ref_list:
            counter +=1
        return counter

async def charge_balance(user, amount):
    decimal_amount = Decimal(str(amount))
    if user.balance < decimal_amount:
        raise DontHaveFunds('Недостаточно средств на балансе!')
    user.balance -= decimal_amount
    user.total_spend += decimal_amount

async def charge_balance_id(user, amount):
    decimal_amount = Decimal(str(amount))
    async with Session() as session:
        async with session.begin():
            user_obj = await session.execute(select(User).where(User.user_id == user))
            user = user_obj.scalar_one_or_none()
            if user.balance < decimal_amount:
                raise DontHaveFunds('Недостаточно средств на балансе!')
            user.balance -= decimal_amount
            user.total_spend += decimal_amount

async def refund_balance(user_id, amount):
    async with Session() as session:
        async with session.begin():
            user_obj = await session.execute(select(User).where(User.user_id == user_id))
            user = user_obj.scalar_one_or_none()
            if not user:
                logging.error(f'Юзеру {user_id} не удалось вернуть деньги')
                raise UserNotRegister('Вы не зарегестрированы! Введите /start для регистрации')
            user.balance += Decimal(str(amount))
            user.total_spend -= Decimal(str(amount))