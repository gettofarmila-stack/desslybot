from logic.api import trade_api


async def check_steam_login(login: str, amount: int):
    resp = await trade_api(login, amount)
    if resp is True:
        return(True)
    else:
        return(False)