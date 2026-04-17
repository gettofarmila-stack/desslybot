from fastapi import APIRouter, HTTPException, Depends
from core.logic.api.steam_refill_api import checking_exchange_rate_api, create_steam_topup_order_api
from core.logic.steam_refill import check_steam_login
from api.utils.security import get_current_user
from utils.exceptions import BotError
from pydantic import BaseModel
from core.database.models import User

class CheckLoginProcess(BaseModel):
    amount: float
    login: str

class SteamRefillOrdering(BaseModel):
    amount: float
    login: str

router = APIRouter(prefix="/steamtopup", tags=["SteamRefill"])

@router.get("/currency_codes")
async def get_all_currency():
    return {
    1: "United States dollar",
    5: "Russian ruble",
    18: "Ukrainian hryvnia",
    37: "Kazakhstani tenge"
}

@router.get('/exchange_rate/{currency}')
async def get_exchange_rate_fastapi(currency: int):
    try:
        rate = await checking_exchange_rate_api(str(currency))
        return {'exchange_rate': rate}
    except BotError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post('/check_login')
async def check_login(data: CheckLoginProcess):
    try:
        return {'can_refill': await check_steam_login(data.login, data.amount)}
    except BotError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post('/topup')
async def steam_topup_order(data: SteamRefillOrdering, user: User = Depends(get_current_user)):
    try:
        return await create_steam_topup_order_api(user.user_id, data.login, data.amount)
    except BotError as e:
        raise HTTPException(status_code=400, detail=str(e))