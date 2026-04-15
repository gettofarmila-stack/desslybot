from aiogram import types, Router, F
from keyboards.payment_menu import payment_builder, payment_check_builder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from logic.payment import create_payment, check_payment
from keyboards.steam_refill_keyboards import inline_main_menu


class PaymentOrdering(StatesGroup):
    waiting_for_amount = State()


router = Router()


@router.callback_query(F.data == 'topup')
async def topup_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_caption(caption='Введите сумму пополнения в USD:')
    await state.set_state(PaymentOrdering.waiting_for_amount)

@router.message(PaymentOrdering.waiting_for_amount)
async def topup_creating_handler(message: types.Message, state: FSMContext):
    amount_str = message.text
    try:
        amount = float(amount_str.replace(',', '.'))
        if amount < 0.1:
            return await message.answer("Минимальная сумма пополенния 0.1$")
    except ValueError:
        await message.answer("Нужно ввести число!")
    payment = await create_payment(message.from_user.id, amount)
    url, payment_id = payment.get('url'), payment.get('payment_id')
    await state.update_data(url=url)
    await message.answer('Платёж создан!', reply_markup=payment_builder(url, payment_id))

@router.callback_query(F.data.startswith('payment_update_'))
async def payment_update_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    url = data.get('url')
    payment_id = int(callback.data.split('_')[-1])
    text = await check_payment(payment_id)
    if 'Успешное пополнение' in text:
        return await callback.message.edit_text(text, reply_markup=inline_main_menu())
    try:
        await callback.message.edit_text(text, reply_markup=payment_builder(url, payment_id))
    except Exception:
        await callback.answer(text)
    else:
        await callback.answer(text)