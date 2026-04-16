from fastapi import APIRouter, Depends
from api.utils.security import get_current_user
from core.database.models import User

router = APIRouter(prefix="/user", tags=["User"])

@router.get("/balance")
async def get_profile(user: User = Depends(get_current_user)):
    return {"balance": user.balance}