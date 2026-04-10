from database.engine import Session
from database.models import Order, User
from utils.exceptions import DontHaveFunds, UserNotRegister
from sqlalchemy import select
from logic.repository.user_rep import charge_balance
import logging

async def create_steam_gift_order(customer_id, api_data, price):
    async with Session() as session:
            async with session.begin():
                user_obj = await session.execute(select(User).where(User.user_id == int(customer_id)).with_for_update())
                user = user_obj.scalar_one_or_none()
                if not user:
                    raise(UserNotRegister('Вы не зарегестрированы!'))
                await charge_balance(amount=price, user=user)
                transaction_id = api_data.get('transaction_id')
                status = api_data.get('status')
                new_order = Order(owner_id=customer_id, transaction_id=transaction_id, status=status)
                session.add(new_order)
            return new_order