from utils.get_cache import VOUCHERS_CACHE
from logic.api.voucher_api import get_voucher_info_api
from utils.exceptions import BotError

def get_voucher_items():
    return [(v.get('name'), v.get('id')) for v in VOUCHERS_CACHE if v.get('name')]

async def get_voucher_variations(voucher_id):
    voucher_info = await get_voucher_info_api(voucher_id)
    variations = voucher_info.get('variations')
    return variations

def variation_info_builder(variations, target_id):
    found_var = None
    for v in variations:
        if v['id'] == int(target_id):
            found_var = v
            break
    if found_var is None:
        raise BotError('Произошла ошибка! Вернитесь в главное меню, и выберите товар снова, если ошибка повторяется то обратитесь в поддержку.')
    return found_var