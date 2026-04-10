import logging
from sqlalchemy import select
from database.engine import Session
from database.models import Order, User
from logic.repository.user_rep import charge_balance
from utils.exceptions import DontHaveFunds, UserNotRegister

async def create_steam_topup_order_db(customer_id: int, transaction_id: str, status: str, amount):
    async with Session() as session:
        async with session.begin():
            user_obj = await session.execute(select(User).where(User.user_id == int(customer_id)).with_for_update())
            user = user_obj.scalar_one_or_none()
            if not user:
                raise UserNotRegister('Вы не зарегестрированы! Пропишите /start')
            await charge_balance(user, amount)
            new_order = Order(owner_id=customer_id, transaction_id=transaction_id, status=status)
            session.add(new_order)
        return new_order