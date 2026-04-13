import logging
from aiogram import types, F, Router
from keyboards.vouchers import voucher_builder, variations_builder, confirm_variation_builder, voucher_history_builder, voucher_history_select_builder
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from logic.vouchers import get_voucher_items, get_voucher_variations, variation_info_builder, voucher_ordering, voucher_text_loader, current_voucher_text_loader
from logic.repository.voucher_rep import get_voucher_history_rep
from keyboards.steam_refill_keyboards import inline_main_menu


class VoucherOrdering(StatesGroup):
    waiting_for_search = State()


router = Router()

@router.callback_query(F.data == 'vouchers')
async def voucher_select_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    data = await state.get_data()
    if data.get('search'):
        voucher_names = data.get('search')
    else:
        voucher_names = get_voucher_items()
        await state.update_data(search=voucher_names)
    await callback.message.answer('Выбери, или найди нужный ваучер:', reply_markup=voucher_builder(voucher_names))
    await callback.answer()

@router.callback_query(F.data.startswith('vouchers_page_'))
async def voucher_page_select_handler(callback: types.CallbackQuery, state: FSMContext):
    page = int(callback.data.split('_')[-1])
    data = await state.get_data()
    voucher_names = data.get('search')        
    await callback.message.edit_text('Выбери, или найди нужный ваучер:', reply_markup=voucher_builder(voucher_names, page))
    await callback.answer()

@router.callback_query(F.data == 'clear_voucher_search')
async def clear_voucher_search_handler(callback: types.CallbackQuery, state: FSMContext):
    vouchers = get_voucher_items()
    await state.update_data(search=vouchers)
    await callback.message.edit_text('Успешно сброшено! Выбери, или найди нужный ваучер:', reply_markup=voucher_builder(vouchers))

@router.callback_query(F.data == 'search_voucher')
async def voucher_search_handler(callback: types.CallbackQuery, state: FSMContext):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text='Назад', callback_data='vouchers', style='danger'))
    builder.row(types.InlineKeyboardButton(text='Главное меню', callback_data='main_menu', style='danger'))
    await callback.message.edit_text('Введите название ваучера, не меньше 3х символов:', reply_markup=builder.as_markup())
    await state.set_state(VoucherOrdering.waiting_for_search)

@router.message(VoucherOrdering.waiting_for_search)
async def voucher_search_input_handler(message: types.Message, state: FSMContext):
    query = message.text.lower()
    if len(query) < 3:
        return await message.answer('Слишком мало символов! Попробуйте снова:')
    all_vouchers = get_voucher_items()
    filtered_vouchers = [v for v in all_vouchers if query in v[0].lower()]
    if not filtered_vouchers:
        return await message.answer('Ничего не найдено... Попробуй другое название:')
    await state.update_data(search=filtered_vouchers)
    await state.set_state(None)
    await message.answer(f'Найдено товаров: {len(filtered_vouchers)}', reply_markup=voucher_builder(filtered_vouchers))

@router.callback_query(F.data.startswith('select_voucher_'))
async def select_current_voucher_handler(callback: types.CallbackQuery, state: FSMContext):
    voucher_id = int(callback.data.split('_')[-1])
    await state.update_data(voucher_id=voucher_id)
    variations = await get_voucher_variations(voucher_id)
    await state.update_data(current_variation=variations)
    await callback.message.edit_text('Выбери тип ваучера:', reply_markup=variations_builder(variations))

@router.callback_query(F.data.startswith('variation_'))
async def get_info_current_variation_handler(callback: types.CallbackQuery, state: FSMContext):
    var_id = callback.data.split('_')[1]
    data = await state.get_data()
    current_var = data.get('current_variation')
    voucher_id = data.get('voucher_id')
    var = variation_info_builder(current_var, var_id)
    await state.update_data(var=var)
    status = "✅ В наличии" if var.get('stock') > 0 else "❌ Нет в наличии"
    await callback.message.edit_text (
        f"<b>{var.get('name')}</b>\n\n"
        f"--- Информация ---\n"
        f"💎 <b>Преимущества:</b> {var.get('benefits')}\n"
        f"📦 <b>Статус:</b> {status} ({var.get('stock')} шт.)\n"
        f"💰 <b>К оплате:</b> <code>{var.get('price')}</code>\n\n"
        f"💰 <b>Валюта:</b> <code>{var.get('currency')}</code>\n\n"
        f"<i>После оплаты ты получишь уникальный код активации.</i>", parse_mode='HTML', reply_markup=confirm_variation_builder(voucher_id, var_id)
    )

@router.callback_query(F.data.startswith('buy_voucher_'))
async def buy_voucher_processing(callback: types.CallbackQuery, state: FSMContext):
    voucher_id = int(callback.data.split('_')[-1])
    var_id = int(callback.data.split('_')[-2])
    data = await state.get_data()
    var_info = data.get('var')
    voucher_info = await voucher_ordering(customer_id=callback.from_user.id, variation_info=var_info, voucher_id=voucher_id, var_id=var_id)
    text = await voucher_text_loader(voucher_info)
    await callback.message.edit_text(text, parse_mode='HTML', reply_markup=inline_main_menu())
    await callback.answer()

@router.callback_query(F.data == 'voucher_order_history')
async def voucher_order_history_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data.get('vouchers'):
        vouchers = data.get('vouchers')
    else:
        vouchers = await get_voucher_history_rep(callback.from_user.id)
        if len(vouchers) == 0:
            return await callback.message.edit_text('Вы ещё не покупали ваучеры!', reply_markup=voucher_history_builder(vouchers))
        await state.update_data(vouchers=vouchers)
    await callback.message.edit_caption(caption='Выбери свой ваучер:', reply_markup=voucher_history_builder(vouchers))

@router.callback_query(F.data.startswith('voucher_page_'))
async def voucher_order_history_page_handler(callback: types.CallbackQuery, state: FSMContext):
    page = int(callback.data.split('_')[-1])
    data = await state.get_data()
    vouchers = data.get('vouchers')
    await callback.message.edit_caption(caption='Выбери свой ваучер:', reply_markup=voucher_history_builder(vouchers, page))
    await callback.answer()

@router.callback_query(F.data.startswith('voucher_history_select_'))
async def select_voucher_history_handler(callback: types.CallbackQuery):
    try:
        voucher_id = int(callback.data.split('_')[-1])
        text = await current_voucher_text_loader(voucher_id)
        await callback.message.edit_caption(caption=text, parse_mode='HTML', reply_markup=voucher_history_select_builder())
        await callback.answer()
    except Exception as e:
        logging.error(f'При выборе ваучер хистори{e}')
        await callback.message.edit_caption(caption=e)