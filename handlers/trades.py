import logging
from aiogram import types, Router, F
from aiogram.filters.command import CommandStart, CommandObject
from logic.trade_logic import check_exchange_rate
from config import SERVICE_NAME
from keyboards.trade_keyboards import trade_select_currency_keyboard, inline_main_menu, confirm_buttons
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup



class RefillProcessing(StatesGroup):
    waiting_for_amount = State()   # Ожидание суммы денег

router = Router()

@router.callback_query(F.data == 'steam_refill')
async def steam_refill_currency_choise_handler(callback: types.CallbackQuery):
    await callback.message.edit_text('Выберите валюту для пополнения:', reply_markup=trade_select_currency_keyboard())
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
    sum_in_usd = await check_exchange_rate(amount=int(message.text), currency=currency)
    if sum_in_usd < 0.1:
        return await message.answer('Слишком маленькая сумма пополнения! Попробуй ещё раз.')
    await message.answer(f'Вы подтверждаете пополнение {sum_in_usd}$ на баланс? (не переживайте за валюту, стиму нет до неё разницы)', reply_markup=confirm_buttons(sum_in_usd))
