import logging
from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from api.utils.security import get_current_user
from core.database.models import User
from core.logic.api.steam_gift_api import get_games_list, get_game_info_api
from core.logic.steam_gift import steam_gift_processing_fastapi
from utils.exceptions import BotError
from api.utils.security import get_db

class SteamGiftData(BaseModel):
    invite_url: str
    package_id: int
    app_id: int
    region: str


router = APIRouter(prefix="/steam_gifts", tags=["SteamGifts"])

@router.get("/steamgift")
async def get_gift_list():
    return await get_games_list()

@router.get('/steamgift/{app_id}')
async def get_current_game_info(app_id: int):
    try:
        game = await get_game_info_api(app_id)
        if not game:
            raise HTTPException(status_code=404, detail="Игра не найдена")
        return game
    except BotError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post('/steamgift/sendgame')
async def send_current_gift(data: SteamGiftData, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    try:
        response = await steam_gift_processing_fastapi(user=user, steam_link=data.invite_url, region=data.region, package_id=data.package_id, app_id=data.app_id)
        return response
    except BotError as e:
        raise HTTPException(status_code=400, detail=str(e))