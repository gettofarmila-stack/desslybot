
import logging
from aiogram import types, Router
from aiogram.filters.command import CommandStart, CommandObject
from logic.repository.user_rep import is_register, registrate_user
from config import SERVICE_NAME
from keyboards.main_menu import main_menu_builder

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message, command: CommandObject=None):
    args = command.args if command else None
    user_id = message.from_user.id
    if not await is_register(user_id):
        ref_id = None
        if args and args.isdigit() and int(args) != user_id:
            ref_id = int(args)
            try:
                await message.bot.send_message(ref_id, f'По вашей реферальной ссылке зашёл {user_id}id.\n Теперь вы получите бонус с его пополнения в виде 1% от суммы каждого его пополнения!')
            except Exception:
                logging.error(f'При регистрации юзера {message.from_user.username}, {user_id}id что-то пошло не так...')
        registrate = await registrate_user(user_id, args)
        await message.answer('Вы успешно зарегестрировались по реферальной ссылке! Теперь ваш друг будет получать бонусы.')
    await message.answer(f'Добро пожаловать {message.from_user.first_name}, мы работаем 24/7!', reply_markup=main_menu_builder())