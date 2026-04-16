import asyncio
import logging
from config import ADMIN_LIST
from core.logic.repository.admin_rep import get_global_stats_rep, get_all_user_ids_rep, delete_user_rep
from core.logic.repository.user_rep import refill_user_balance_rep, charge_balance_id, get_user_object
from core.database.engine import Session
from aiogram.exceptions import TelegramRetryAfter, TelegramForbiddenError
from utils.exceptions import BotError


def is_admin(uid):
    return uid in ADMIN_LIST

async def get_global_stats():
    async with Session() as session:
        objects = await get_global_stats_rep(session)
        users, transactions = objects.get('users'), objects.get('transactions')
        user_counter = len(users)
        transaction_counter = len(transactions)
        user_balances = sum(float(user.balance) for user in users)
        transaction_total = sum(float(transaction.amount) for transaction in transactions)
        return (
            '<b>СТАТИСТИКА</b>\n'
            '1) Люди:\n\n'
            f'Людей зарегестрировано: <b>{user_counter}</b>\n'
            f'Общий баланс: <b>{user_balances:.2f}</b>\n'
            '2) Пополнения:\n\n'
            f'Всего пополнений: <b>{transaction_counter}</b>\n'
            f'Грязными заработано: <b>{transaction_total:.2f}$</b>\n'
        )
    
async def start_broadcast(bot, text):
    count = 0
    blocked = 0
    async with Session() as session:
        user_ids = await get_all_user_ids_rep(session)
    for user_id in user_ids:
        try:
            await bot.send_message(user_id, text)
            count += 1
            await asyncio.sleep(0.05)
        except TelegramForbiddenError:
            blocked += 1
        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after)
            await bot.send_message(user_id, text)
            count += 1
        except Exception as e:
            logging.error(f'Ошибка при рассылке на ID: {user_id}. Ошибка: {e}')
    return {'count': count, 'blocked': blocked}

async def broadcast_manage(bot, text):
    stats = await start_broadcast(bot, text)
    count, blocked = stats.get('count', 0), stats.get('blocked', 0)
    return (
        '<b>📊 СТАТИСТИКА РАССЫЛКИ</b>\n\n'
        f'✅ Успешно доставлено: <b>{count}</b>\n'
        f'🚫 Заблокировали бота: <b>{blocked}</b>'
    )

async def refill_user_balance(user_id, amount):
    async with Session() as session:
        async with session.begin():
            try:
                await refill_user_balance_rep(session, amount, user_id)
                return(f'Успешно пополнено юзеру ID: {user_id} на {amount}$')
            except Exception as e:
                logging.error(f'Произошла ошибка: {e}')
                raise BotError(f'Ошибка: {e}')
            
async def charge_user_balance_admin(user_id, amount):
    try:
        await charge_balance_id(user_id, amount)
        return(f'Успешно списано с юзера ID: {user_id}, {amount}$')
    except Exception as e:
        logging.error(f'Произошла ошибка: {e}')
        raise BotError(f'Ошибка: {e}')
    
async def get_user_stats_admin(user_id):
    user = await get_user_object(user_id)
    return(
        f'СТАТИСТИКА ID: {user_id}\n'
        f'Баланс: {user.balance}\n'
        f'Всего потрачено: {user.total_spend}'
    )

async def delete_user_admin(user_id):
    async with Session() as session:
        async with session.begin():
            try:
                await delete_user_rep(user_id, session)
                return('Успешно удалено!')
            except Exception as e:
                logging.error(f'Ошибка: {e}')
                return f"Ошибка при удалении: {e}"