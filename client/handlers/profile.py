from client.keyboards.profile_menu import profile_builder, order_history_builder, referral_system_builder, developer_menu_builder
from aiogram import types, Router, F, Bot
from core.logic.user_logic import profile_text_builder, get_referral_link, developer_menu, delete_api_key
from core.logic.repository.user_rep import get_user_referrals
from aiogram.fsm.context import FSMContext


router = Router()

@router.callback_query(F.data == 'profile')
async def profile_handler(callback: types.CallbackQuery):
    text = await profile_text_builder(callback.from_user.id)
    await callback.message.edit_caption(caption=text, reply_markup=profile_builder())
    await callback.answer()

@router.callback_query(F.data == 'order_history')
async def order_history_handler(callback: types.CallbackQuery):
    await callback.message.edit_caption(caption='Выберите нужный архив:', reply_markup=order_history_builder())
    await callback.answer()

@router.callback_query(F.data == 'referral_system')
async def referral_system_handler(callback: types.CallbackQuery, bot: Bot):
    ref_counter = await get_user_referrals(callback.from_user.id)
    bot_user = await bot.get_me()
    ref_link = get_referral_link(callback.from_user.id, bot_user.username)
    await callback.message.edit_caption(caption=f'Ваша реферальная ссылка:\n<code>{ref_link}</code>', parse_mode='HTML', reply_markup=referral_system_builder(ref_counter))
    await callback.answer()

@router.callback_query(F.data == 'developer_panel')
async def developer_panel_handler(callback: types.CallbackQuery):
    await callback.message.delete()
    text = await developer_menu(callback.from_user.id)
    await callback.message.answer(text, parse_mode='HTML', reply_markup=developer_menu_builder())
    await callback.answer()

@router.callback_query(F.data == 'api_key_reload')
async def developer_panel_api_reload_handler(callback: types.CallbackQuery):
    uid = callback.from_user.id
    await delete_api_key(uid)
    text = await developer_menu(uid)
    await callback.message.edit_text(f'Ключ сброшен\n\n{text}', parse_mode='HTML', reply_markup=developer_menu_builder())
    await callback.answer()