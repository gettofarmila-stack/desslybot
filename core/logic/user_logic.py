
from core.logic.repository.user_rep import get_user_object

async def profile_text_builder(uid):
    user = await get_user_object(uid)
    return(
        f'Профиль\n' 
        f'Баланс: {user.balance}\n' 
        f'Всего потрачено: {user.total_spend}'
    )

def get_referral_link(uid, bot):
    return f'https://t.me/{bot}?start={uid}'