from aiogram import types, F, Router
from keyboards.steam_gifts import games_builder
from keyboards.steam_refill_keyboards import inline_main_menu
from utils.gift_games_list import GAMES_CACHE
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from logic.steam_gift import searching_games
class GameSearching(StatesGroup):
    waiting_for_game = State()

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
    builder.row(types.InlineKeyboardButton(text='Назад к играм (сбрасывает поиск)', callback_data='steam_gifts', style='danger'))
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