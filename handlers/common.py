
import logging
from aiogram import types, Router, F
from aiogram.types import InputMediaPhoto
from aiogram.filters.command import CommandStart, CommandObject, Command
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
                logging.error(f'При регистрации юзера {message.from_user.username}, ID: {user_id} что-то пошло не так...')
        registrate = await registrate_user(user_id, args)
        await message.answer('Успешная регистрация!')
    photo = 'AgACAgQAAxkBAANvaddiaCdKNqlPQ37m_We4Xp0KFcsAAigNaxsY08BS6iU2QfZy8-gBAAMCAAN5AAM7BA'
    await message.answer_photo(photo=photo, caption=f'Добро пожаловать {message.from_user.first_name}, мы работаем 24/7!', reply_markup=main_menu_builder())

@router.callback_query(F.data == 'main_menu')
async def main_menu_callback(callback: types.CallbackQuery):
    photo = 'AgACAgQAAxkBAANvaddiaCdKNqlPQ37m_We4Xp0KFcsAAigNaxsY08BS6iU2QfZy8-gBAAMCAAN5AAM7BA'
    await callback.message.edit_media(media=InputMediaPhoto(media=photo, caption=f'Добро пожаловать {callback.from_user.first_name}, мы работаем 24/7!'), reply_markup=main_menu_builder())
    await callback.answer()

@router.message(Command("getid"))
async def get_photo_id(message: types.Message):
    if message.photo:
        photo_id = message.photo[-1].file_id
        await message.answer(f"<code>{photo_id}</code>", parse_mode="HTML")
        await message.answer("Это айди твоей фотки")
    else:
        await message.answer("Прикрепи картинку к сообщению вместе с командой")