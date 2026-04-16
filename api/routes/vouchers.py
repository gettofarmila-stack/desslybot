from fastapi import APIRouter, Depends
from api.utils.security import get_current_user
from core.database.models import User

router = APIRouter(prefix="/vouchers", tags=["Vouchers"])

@router.get("/get_vouchers")
async def get_vouchers():
    pass