from fastapi import APIRouter, Depends
from api.utils.security import get_current_user
from core.database.models import User

router = APIRouter(prefix="/steam_refill", tags=["SteamRefill"])

@router.get("/get_exchange_rate")
async def get_vouchers():
    pass