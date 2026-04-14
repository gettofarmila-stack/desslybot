from keyboards.profile_menu import profile_builder, order_history_builder, referral_system_builder
from aiogram import types, Router, F, Bot
from logic.user_logic import profile_text_builder, get_referral_link
from logic.repository.user_rep import get_user_referrals
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
