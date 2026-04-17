from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from api.utils.security import get_current_user, get_db
from core.logic.api.voucher_api import get_vouchers_api, get_voucher_info_api
from core.logic.vouchers import voucher_ordering_fastapi
from core.database.models import User
from utils.exceptions import BotError

router = APIRouter(prefix="/voucher", tags=["Vouchers"])

class BuyVoucherOrder(BaseModel):
    root_id: int
    variant_id: int

@router.get("/products")
async def get_vouchers():
    return await get_vouchers_api()

@router.get('/products/{voucher_id}')
async def get_current_voucher(voucher_id: int):
    try:
        return await get_voucher_info_api(voucher_id)
    except BotError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post('/buy')
async def buy_voucher(data: BuyVoucherOrder, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    try:
        response = await voucher_ordering_fastapi(user, data.root_id, data.variant_id, db)
        return response
    except BotError as e:
        raise HTTPException(status_code=400, detail=str(e))