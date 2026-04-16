from fastapi import APIRouter, Depends, HTTPException
from api.utils.security import get_current_user
from core.database.models import User
from core.logic.api.steam_gift_api import get_games_list, get_game_info_api
from utils.exceptions import BotError

router = APIRouter(prefix="/steam_gifts", tags=["SteamGifts"])

@router.get("/games")
async def get_gift_list():
    return await get_games_list()

@router.get('/games/{app_id}')
async def get_current_game_info(app_id: int):
    try:
        game = await get_game_info_api(app_id)
        if not game:
            raise HTTPException(status_code=404, detail="Игра не найдена")
        return game
    except BotError as e:
        raise HTTPException(status_code=400, detail=str(e))