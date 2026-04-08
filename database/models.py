import asyncio
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, Integer, String, BigInteger, DateTime, Numeric, ForeignKey
from datetime import datetime
from database.engine import engine

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, unique=True)
    referrer_id = Column(BigInteger)
    reg_date = Column(DateTime, default=datetime.now)
    balance = Column(Numeric(10, 2), default=0.00)
    orders = relationship('Order', back_populates='user')

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    owner_id = Column(BigInteger, ForeignKey('users.user_id'))
    transaction_id = Column(String)
    attributes = Column(String)
    amount = Column(Numeric(10, 4), default=0.0000)
    commission = Column(Numeric(10, 4), default=0.0000)
    final_amount = Column(Numeric(10, 4), default=0.0000)
    type = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    description = Column(String)

    user = relationship('User', back_populates='orders')

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(init_models())