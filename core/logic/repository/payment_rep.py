
import logging
from core.database.engine import Session
from core.database.models import Transaction
from utils.exceptions import BotError
from sqlalchemy import delete, select


async def create_payment_rep(session, user_id, amount):
        new_transaction = Transaction(owner_id=user_id, amount=amount)
        session.add(new_transaction)
        await session.flush()
        return new_transaction
    
async def update_payment_rep(session, payment_id, uuid, payment_status):
        payment = await session.get(Transaction, payment_id)
        if payment:
            payment.uuid = uuid
            payment.payment_status = payment_status
        else:
            logging.error(f'При обновлении данных платежа, платёж не был найден')
            raise BotError('Ошибка при обновлении платежа, попробуйте снова, а затем обратитесь в поддержку.')
            
async def delete_payment_rep(payment_id):
    async with Session() as session:
        await session.execute(delete(Transaction).where(Transaction.id == int(payment_id)))
        await session.commit()

async def get_payment_info_rep(session, payment_id):
    payment = await session.execute(select(Transaction).where(Transaction.id == payment_id))
    return payment.scalar_one_or_none()

