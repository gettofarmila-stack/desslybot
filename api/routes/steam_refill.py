from fastapi import APIRouter, HTTPException
from core.logic.api.steam_refill_api import checking_exchange_rate_api
from utils.exceptions import BotError

router = APIRouter(prefix="/steam_refill", tags=["SteamRefill"])

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