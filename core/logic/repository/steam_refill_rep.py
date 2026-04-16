import logging
from sqlalchemy import select, delete
from core.database.engine import Session
from core.database.models import Order, User
from core.logic.repository.user_rep import charge_balance
from utils.exceptions import DontHaveFunds, UserNotRegister, BotError

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
    
async def update_order_status_db(order_id, transaction_id, status):
    async with Session() as session:
        async with session.begin():
            result = await session.execute(select(Order).where(Order.id == order_id).with_for_update())
            order = result.scalar_one_or_none()
            if not order:
                logging.error(f'Заказ {order_id} не найден в БД')
                raise BotError('Ошибка БД, обратитесь в поддержку')
            order.transaction_id = transaction_id
            order.status = status

async def delete_order_db(order_id):
    async with Session() as session:
        async with session.begin():
            order = await session.execute(delete(Order).where(Order.id == order_id))