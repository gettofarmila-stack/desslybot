from sqlalchemy import select
from database.engine import Session
from database.models import Voucher


async def add_voucher_info(owner_id, transaction_id, status, voucher_name, voucher_info):
    async with Session() as session:
        async with session.begin():
            new_voucher = Voucher(owner_id=owner_id, transaction_id=transaction_id, status=status, voucher_name=voucher_name, voucher=voucher_info)
            session.add(new_voucher)
            await session.flush()
            await session.refresh(new_voucher)
        return new_voucher
    
