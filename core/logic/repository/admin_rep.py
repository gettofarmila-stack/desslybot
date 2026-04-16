from core.database.models import User, Transaction
from sqlalchemy import select
from utils.exceptions import BotError

async def get_global_stats_rep(session):
    users_obj = await session.execute(select(User))
    users = users_obj.scalars().all()
    transactions_obj = await session.execute(select(Transaction))
    transactions = transactions_obj.scalars().all()
    return {'users': users, 'transactions': transactions}

async def get_all_user_ids_rep(session):
    user_obj = await session.execute(select(User.user_id))
    users = user_obj.scalars().all()
    return users

async def delete_user_rep(user_id, session):
    try:
        user_obj = await session.execute(select(User).where(User.user_id == int(user_id)))
        user = user_obj.scalar_one_or_none()
        user.balance = 0.00
        user.total_spend = 0.00
    except Exception as e:
        raise BotError(f'Не удалось удалить юзера: {e}')