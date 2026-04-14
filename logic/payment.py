from logic.api.payment_api import create_payment_api, check_payment_api
from logic.repository.payment_rep import create_payment_rep, update_payment_rep, get_payment_info_rep
from logic.repository.user_rep import refill_user_balance_rep
from utils.exceptions import BotError
from database.engine import Session
from decimal import Decimal
import logging

async def create_payment(uid, raw_amount):
    amount = Decimal(raw_amount).quantize(Decimal('0.00'))
    async with Session() as session:
        try:
            payment = await create_payment_rep(session, uid, amount)
            payment_id = payment.id
            data = await create_payment_api(amount, payment_id)
            if data and data.get('uuid'):
                await update_payment_rep(session, payment_id, data['uuid'], data['payment_status'])
                await session.commit()
                return {'url': data.get('url'), 'payment_id': payment_id}
            else:
                await session.rollback()
                raise BotError('Платежка не вернула данные')
        except Exception as e:
            await session.rollback()
            logging.error(f"Ошибка: {e}")
            raise BotError('Ошибка при создании платежа. Попробуйте позже.')
        
async def check_payment(payment_id):
    async with Session() as session:
        try:
            async with session.begin():
                payment = await get_payment_info_rep(session, payment_id)
                uuid = payment.uuid
                data = await check_payment_api(uuid, payment_id)
                payment.payment_status = data.get('payment_status')
                if payment.payment_status == 'paid':
                    await refill_user_balance_rep(session, amount=payment.amount, user_id=payment.owner_id)
                    return(f'Успешное пополнение на сумму {payment.amount}')
                return('Платёж не найден! После оплаты немного подождите...')
        except Exception as e:
            logging.error(f'Ошибка в check_payment: {e}')
            raise BotError('Ошибка при проверке платежа!')