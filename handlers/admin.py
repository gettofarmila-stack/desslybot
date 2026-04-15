from aiogram import types, Router, F, Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder
from logic.admin import is_admin, get_global_stats, broadcast_manage, refill_user_balance, charge_user_balance_admin, get_user_stats_admin, delete_user_admin
from keyboards.main_menu import back_to_admin_panel_builder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.steam_refill_keyboards import inline_main_menu

class RefillProcessing(StatesGroup):
    waiting_for_broadcast_text = State()
    waiting_uid = State()
    waiting_for_amount = State()

class ChargeProcessing(StatesGroup):
    waiting_uid = State()
    waiting_for_amount = State()

class GetStatsProcessing(StatesGroup):
    waiting_uid = State()

class DeleteUserProcessing(StatesGroup):
    waiting_uid = State()

router = Router()

@router.callback_query(F.data == 'admin_panel')
async def admin_panel_handler(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        return await callback.answer('Тебе тут не место')
    await callback.answer()
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text='Статистика', callback_data='admin_stats', style='primary'),
        types.InlineKeyboardButton(text='Рассылка', callback_data='admin_broadcast', style='primary')
    )
    builder.row(
        types.InlineKeyboardButton(text='Выдать баланс', callback_data='admin_refill_user_balance', style='primary'),
        types.InlineKeyboardButton(text='Забрать баланс', callback_data='admin_charge_user_balance', style='primary')
    )
    builder.row(
        types.InlineKeyboardButton(text='Статистика юзера', callback_data='admin_get_user_stats', style='primary'),
        types.InlineKeyboardButton(text='Обнулить юзера', callback_data='admin_delete_user', style='primary')
    )
    builder.row(types.InlineKeyboardButton(text='Главное меню', callback_data='main_menu', style='danger'))
    await callback.message.answer('Добро пожаловать', reply_markup=builder.as_markup())
    await callback.answer()

@router.callback_query(F.data == 'admin_stats')
async def get_global_stats_handler(callback: types.CallbackQuery):
    text = await get_global_stats()
    await callback.message.edit_text(text, parse_mode='HTML', reply_markup=back_to_admin_panel_builder())
    await callback.answer()

@router.callback_query(F.data == 'admin_broadcast')
async def broadcast_configure_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Введите текст рассылки:', reply_markup=inline_main_menu())
    await state.set_state(RefillProcessing.waiting_for_broadcast_text)

@router.message(RefillProcessing.waiting_for_broadcast_text)
async def broadcast_start_handler(message: types.Message, state: FSMContext, bot: Bot):
    text = message.text
    result = await broadcast_manage(bot=bot, text=text)
    await message.answer(result, parse_mode='HTML', reply_markup=inline_main_menu())
    await state.clear()

@router.callback_query(F.data == 'admin_refill_user_balance')
async def admin_refill_user_balance_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Введите user id:', reply_markup=inline_main_menu())
    await callback.answer()
    await state.set_state(RefillProcessing.waiting_uid)

@router.message(RefillProcessing.waiting_uid)
async def admin_refill_user_balance_first_processing_handler(message: types.Message, state: FSMContext):
    uid = message.text
    await state.update_data(user_id=uid)
    await message.answer('Успешно задан айди юзера! Теперь введите сумму пополнения:', reply_markup=inline_main_menu())
    await state.set_state(RefillProcessing.waiting_for_amount)

@router.message(RefillProcessing.waiting_for_amount)
async def admin_refill_user_balance_second_processing_handler(message: types.Message, state: FSMContext):
    amount = message.text
    data = await state.get_data()
    uid = data.get('user_id')
    text = await refill_user_balance(uid, amount)
    await message.answer(text, reply_markup=inline_main_menu())
    await state.clear()

@router.callback_query(F.data == 'admin_charge_user_balance')
async def admin_charge_user_balance_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Введите айди юзера:', reply_markup=inline_main_menu())
    await callback.answer()
    await state.set_state(ChargeProcessing.waiting_uid)

@router.message(ChargeProcessing.waiting_uid)
async def admin_charge_user_balance_first_handler(message: types.Message, state: FSMContext):
    user_id = message.text
    await state.update_data(user_id=user_id)
    await message.answer('Успешно задан айди юзера! Теперь введите сумму списания:', reply_markup=inline_main_menu())
    await state.set_state(ChargeProcessing.waiting_for_amount)

@router.message(ChargeProcessing.waiting_for_amount)
async def admin_charge_user_balance_second_handler(message: types.Message, state: FSMContext):
    amount = message.text
    data = await state.get_data()
    uid = data.get('user_id')
    text = await charge_user_balance_admin(uid, amount)
    await message.answer(text, reply_markup=inline_main_menu())

@router.callback_query(F.data == 'admin_get_user_stats')
async def admin_get_user_stats_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Введите айди юзера, стату которого хотите посмотреть:', reply_markup=inline_main_menu())
    await callback.answer()
    await state.set_state(GetStatsProcessing.waiting_uid)

@router.message(GetStatsProcessing.waiting_uid)
async def admin_get_user_stats_processing_handler(message: types.Message, state: FSMContext):
    uid = message.text
    text = await get_user_stats_admin(uid)
    await message.answer(text, reply_markup=inline_main_menu())

@router.callback_query(F.data == 'admin_delete_user')
async def admin_delete_user_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Введите айди юзера, которого хотите удалить. ОСТОРОЖНО! БЕЗВОЗРАТНОЕ УДАЛЕНИЕ!!!:', reply_markup=inline_main_menu())
    await callback.answer()
    await state.set_state(DeleteUserProcessing.waiting_uid)

@router.message(DeleteUserProcessing.waiting_uid)
async def admin_delete_user_processing_handler(message: types.Message, state: FSMContext):
    uid = message.text
    text = await delete_user_admin(uid)
    await message.answer(text, reply_markup=inline_main_menu())