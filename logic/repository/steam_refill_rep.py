import logging
from sqlalchemy import select
from database.engine import Session
from database.models import Order, User

class DontHaveFunds(Exception):
    pass

async def charge_balance(user, amount):
    if user.balance < amount:
        raise DontHaveFunds('Недостаточно средств на балансе!')
    user.balance -= amount

async def create_steam_topup_order_db(customer_id: int, transaction_id: str, status: str, amount):
    async with Session() as session:
        try:
            async with session.begin():
                user_obj = await session.execute(select(User).where(User.user_id == customer_id).with_for_update())
                user = user_obj.scalar_one_or_none()
                if not user:
                    return 'Юзер не найден'
                await charge_balance(user, amount)
                new_order = Order(owner_id=customer_id, transaction_id=transaction_id, status=status)
                session.add(new_order)
            return new_order
        except DontHaveFunds:
            return 'Недостаточно средств! Пополни баланс'
        except Exception as e:
            logging.warning(f'Ошибка БД при создании заказа: {e}')
            return 'В базе данных произошла ошибка, напиши в поддержку'