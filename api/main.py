from fastapi import FastAPI
from api.routes.user import router as user_router
from api.routes.steam_gifts import router as steam_gifts_router
from api.routes.steam_refill import router as steam_refill_router
from api.routes.vouchers import router as vouchers_router

app = FastAPI(title="DesslyBot API")

app.include_router(user_router)
app.include_router(steam_gifts_router)
app.include_router(steam_refill_router)
app.include_router(vouchers_router)

@app.get("/")
async def root():
    return {"message": "API is working"}