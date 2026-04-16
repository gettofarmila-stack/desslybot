
import secrets
import logging
from core.logic.repository.user_rep import get_user_object, get_user_object_session
from core.database.engine import Session
from utils.exceptions import BotError, UserNotRegister


async def profile_text_builder(uid):
    user = await get_user_object(uid)
    return(
        f'Профиль\n' 
        f'Баланс: {user.balance}\n' 
        f'Всего потрачено: {user.total_spend}'
    )

def get_referral_link(uid, bot):
    return f'https://t.me/{bot}?start={uid}'

def api_key_generator(user):
    try:
        if not user:
            raise UserNotRegister('Юзер не зарегестрирован!')
        user.api_key = secrets.token_urlsafe(32)
    except Exception as e:
        logging.error(f'При генерации ключа произошла ошибка: {e}')
        raise BotError('Ошибка генерации ключа')
            
async def developer_menu(user_id):
    async with Session() as session:
        async with session.begin():
            try:
                user = await get_user_object_session(user_id, session)
                if not user.api_key:
                    api_key_generator(user)
                    return f'Ваш ключ: <code>{user.api_key}</code>'
                return f'Ваш ключ: <code>{user.api_key}</code>'
            except Exception as e:
                logging.error(f'Ошибка API ключа: {e}')
                raise BotError('Ошибка ключа')
            
async def delete_api_key(user_id):
    async with Session() as session:
        async with session.begin():
            user = await get_user_object_session(user_id, session)
            user.api_key = None