from sqlalchemy import select
from core.database.engine import Session
from core.database.models import Voucher


async def add_voucher_info(owner_id, transaction_id, status, voucher_name, voucher_info):
    async with Session() as session:
        async with session.begin():
            new_voucher = Voucher(owner_id=owner_id, transaction_id=transaction_id, status=status, voucher_name=voucher_name, voucher=voucher_info)
            session.add(new_voucher)
            await session.flush()
            await session.refresh(new_voucher)
        return new_voucher
    
async def get_voucher_history_rep(uid):
    async with Session() as session:
        vouchers_obj = await session.execute(select(Voucher).where(Voucher.owner_id == int(uid)))
        vouchers = vouchers_obj.scalars().all()
        return vouchers
    
async def get_current_voucher(voucher_id):
    async with Session() as session:
        voucher_obj = await session.execute(select(Voucher).where(Voucher.id == int(voucher_id)))
        voucher = voucher_obj.scalar_one_or_none()
        return voucher