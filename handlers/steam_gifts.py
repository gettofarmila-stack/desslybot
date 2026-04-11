from aiogram import types, F, Router
from keyboards.steam_gifts import games_builder, editions_builder, regions_builder
from keyboards.steam_refill_keyboards import inline_main_menu
from utils.get_cache import GAMES_CACHE
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from logic.steam_gift import searching_games, game_info_rendering, steam_order_processing
from config import INVITE_LINK_PHOTO
from aiogram.types import InputMediaPhoto
class GameSearching(StatesGroup):
    waiting_for_game = State()
    waiting_friend_link = State()

router = Router()



@router.callback_query(F.data == 'steam_gifts')
async def games_rendering(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Выберите нужную вам игру:', reply_markup=games_builder())

@router.callback_query(F.data.startswith('games_page_'))
async def games_page_rendering(callback: types.CallbackQuery, state: FSMContext):
    page = int(callback.data.split('_')[-1])
    data = await state.get_data()
    search_results = data.get('games_list')
    current_list = search_results if search_results else GAMES_CACHE
    await callback.message.edit_text('Выберите нужную вам игру:', reply_markup=games_builder(all_games=current_list, page=page))

@router.callback_query(F.data == 'search_by_name')
async def game_search_waiting(callback: types.CallbackQuery, state: FSMContext):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text='Назад к играм', callback_data='steam_gifts', style='danger'))
    builder.row(types.InlineKeyboardButton(text='Главное меню', callback_data='main_menu', style='danger'))
    await callback.message.edit_text('Введите название игры, не меньше 3х символов', reply_markup=builder.as_markup())
    await state.set_state(GameSearching.waiting_for_game)
    
@router.message(GameSearching.waiting_for_game)
async def game_search_rendering(message: types.Message, state: FSMContext):
    game_name = message.text
    if len(game_name) < 3:
        return await message.answer('Не меньше 3х символов! Попробуй ещё')
    games = await searching_games(game_name=game_name, games_list=GAMES_CACHE)
    if not games:
        return await message.answer('Ничего не найдено, попробуй другое название!')
    await state.update_data(games_list=games)
    await message.answer(f'Найдено игр: {len(games)}. Выберите нужную:', reply_markup=games_builder(games, page=0))

@router.callback_query(F.data.startswith('buy_game_'))
async def buy_gift_select_edition_handler(callback: types.CallbackQuery, state: FSMContext):
    app_id = callback.data.split('_')[-1]
    data = await game_info_rendering(app_id)
    if data:
        await state.update_data(full=data)
    await callback.message.edit_text('Выбери издание:', reply_markup=editions_builder(data))
    await callback.answer()

@router.callback_query(F.data.startswith('edition_'))
async def buy_gift_select_region_handler(callback: types.CallbackQuery, state: FSMContext):
    package_id = int(callback.data.split('_')[1])
    raw_data = await state.get_data()
    full_dict = raw_data.get('full')
    if not full_dict or not isinstance(full_dict, dict):
        return await callback.answer("Данные устарели, выберите игру заново", show_alert=True)
    reg_list = full_dict.get('reg_info', [])
    await callback.message.edit_text('Выбери регион покупки:', reply_markup=regions_builder(reg_list, package_id))
    await callback.answer()

@router.callback_query(F.data == 'back_to_editions')
async def back_to_editions_handler(callback: types.CallbackQuery, state: FSMContext):
    raw_data = await state.get_data()
    data = raw_data.get('full')
    if not data:
        return await callback.answer("Данные потерялись, начни поиск заново", show_alert=True)
    await callback.message.edit_text('Выбери издание:', reply_markup=editions_builder(data))
    await callback.answer()

@router.callback_query(F.data == 'clear_search')
async def clear_search_handler(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(games_list=None)
    await callback.answer('Успешно сброшено, перелистните страницу')

@router.callback_query(F.data.startswith('gift_'))
async def take_user_steam_link(callback: types.CallbackQuery, state: FSMContext):
    region = callback.data.split('_')[1]
    package_id = callback.data.split('_')[2]
    price = callback.data.split('_')[3]
    await state.update_data(region=region, package_id=package_id, price=price)
    await callback.message.edit_media(media=InputMediaPhoto(media=INVITE_LINK_PHOTO, caption='Отправьте вашу быструю ссылку на дружбу в формате s.team/p/...'), reply_markup=inline_main_menu())
    await state.set_state(GameSearching.waiting_friend_link)

@router.message(GameSearching.waiting_friend_link)
async def order_confirm_handler(message: types.Message, state: FSMContext):
    await message.delete()
    if not 's.team/p/' in message.text:
        return await message.answer('Проверьте вашу ссылку! Она должна быть формата s.team/p/')
    raw_data = await state.get_data()
    region = raw_data.get('region')
    package_id = raw_data.get('package_id')
    price = raw_data.get('price')
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text='Подтвердить', callback_data=f'confirm_{message.text}_{region}_{package_id}', style='success'))
    builder.row(types.InlineKeyboardButton(text='Главное меню', callback_data='main_menu', style='danger'))
    await message.answer(f'Вы уверены, что хотите купить данный товар на сумму {price}$?', reply_markup=builder.as_markup())

@router.callback_query(F.data.startswith('confirm_'))
async def order_processing_handler(callback: types.CallbackQuery, state: FSMContext):
    formatter = callback.data.split('_')
    steam_link = formatter[1]
    region = formatter[2]
    package_id = formatter[3]
    raw_data = await state.get_data()
    price = raw_data.get('price')
    result = await steam_order_processing(uid=callback.from_user.id, steam_link=steam_link, region=region, package_id=package_id, price=price)
    await callback.message.edit_text(result, reply_markup=inline_main_menu())
    await callback.answer()