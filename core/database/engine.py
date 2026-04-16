from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from config import POSTGRES_URL

engine = create_async_engine(POSTGRES_URL)
Session = async_sessionmaker(bind=engine, expire_on_commit=False)