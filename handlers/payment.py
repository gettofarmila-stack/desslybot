from aiogram import types, Router, F
from keyboards.payment_menu import payment_builder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from logic.payment import create_payment


class PaymentOrdering(StatesGroup):
    waiting_for_amount = State()


router = Router()


@router.callback_query(F.data == 'topup')
async def topup_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_caption(caption='Введите сумму пополнения в USD:')
    await state.set_state(PaymentOrdering.waiting_for_amount)

@router.message(PaymentOrdering.waiting_for_amount)
async def topup_creating_handler(message: types.Message, state: FSMContext):
    amount = int(message.text)
    if amount < 1:
        return await message.answer(caption='Слишком маленькая сумма пополнения! Не меньше 1$!')
    payment = await create_payment(message.from_user.id, amount)
    url, payment_id = payment.get('url'), payment.get('payment_id')
    await message.answer('Платёж создан!', reply_markup=payment_builder(url, payment_id))