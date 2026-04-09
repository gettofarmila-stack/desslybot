
from aiogram import types, Router, F
from aiogram.types import InputMediaPhoto
from logic.trade_logic import check_exchange_rate, create_steam_topup_order
from config import LOGIN_PHOTO, CONFIRM_PHOTO, ERROR_PHOTO
from keyboards.trade_keyboards import trade_select_currency_keyboard, inline_main_menu, confirm_buttons, confirm_buttons_login
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup



class RefillProcessing(StatesGroup):
    waiting_for_login = State()
    waiting_for_amount = State()   # Ожидание суммы денег

router = Router()

@router.callback_query(F.data == 'steam_refill')
async def steam_refill_login_waiting(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_media(media=InputMediaPhoto(media=LOGIN_PHOTO, caption="Введите ваш логин Steam:"), reply_markup=inline_main_menu())
    await state.set_state(RefillProcessing.waiting_for_login)
    await callback.answer()

@router.message(RefillProcessing.waiting_for_login)
async def steam_refill_login_handler(message: types.Message, state: FSMContext):
    login = message.text
    await state.update_data(user_login=login)
    await message.answer_photo(photo=CONFIRM_PHOTO, caption=f'Ваш логин: {login}, вы уверены?', reply_markup=confirm_buttons_login())

@router.callback_query(F.data == 'currency_choise')
async def steam_refill_currency_choise_handler(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Выберите валюту для пополнения:', reply_markup=trade_select_currency_keyboard())
    await callback.answer()

@router.callback_query(F.data.startswith('currency_'))
async def steam_refill_choise_amount_handler(callback: types.CallbackQuery, state: FSMContext):
    currency_id = callback.data.split('_')[1]
    await callback.message.edit_text('Введите сумму пополнения:', reply_markup=inline_main_menu())
    await state.set_state(RefillProcessing.waiting_for_amount)
    await state.update_data(user_currency=currency_id)
    await callback.answer()

@router.message(RefillProcessing.waiting_for_amount)
async def steam_refill_amount_handler(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer('Нужно писать цифры! Попробуй ещё раз.')
    data = await state.get_data()
    currency = data.get('user_currency')
    login = data.get('user_login')
    sum_in_usd = await check_exchange_rate(amount=float(message.text), currency=currency)
    if sum_in_usd < 0.1:
        return await message.answer('Слишком маленькая сумма пополнения! Попробуй ещё раз.')
    await message.answer(f'Вы подтверждаете пополнение {sum_in_usd}$ на баланс? (не переживайте за валюту, стиму нет до неё разницы)', reply_markup=confirm_buttons(sum_in_usd, login))

@router.callback_query(F.data.startswith('confirm_refill_'))
async def steam_refill_ordering_handler(callback: types.CallbackQuery, state: FSMContext):
    order_amount = float(callback.data.split('_')[-2])
    order_login = callback.data.split('_')[-1]
    order = await create_steam_topup_order(customer_id=callback.from_user.id, login=order_login, amount=order_amount)
    if not 'успешно создан' in order:
        return await callback.message.edit_media(media=InputMediaPhoto(media=ERROR_PHOTO, caption=order), reply_markup=inline_main_menu())
    await callback.message.edit_text(order, reply_markup=inline_main_menu())