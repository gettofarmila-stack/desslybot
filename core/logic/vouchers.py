import logging
from utils.get_cache import VOUCHERS_CACHE
from core.logic.api.voucher_api import get_voucher_info_api, buy_voucher_api
from utils.exceptions import BotError
from core.logic.repository.user_rep import charge_balance_id, refund_balance
from core.logic.repository.voucher_rep import add_voucher_info, get_current_voucher

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

async def voucher_ordering(customer_id, variation_info, voucher_id, var_id):
    price = variation_info.get('price')
    charged = False
    try:
        name = variation_info.get('name')
        await charge_balance_id(user=customer_id, amount=price)
        charged = True
        voucher_order_info = await buy_voucher_api(voucher_id=voucher_id, var_id=var_id)
        transaction_id, status, voucher_info = voucher_order_info.get('transaction_uuid'), voucher_order_info.get('status'), voucher_order_info.get('vouchers')
        return await add_voucher_info(owner_id=customer_id, transaction_id=transaction_id, status=status, voucher_name=name, voucher_info=voucher_info)
    except Exception as e:
        if charged is True:
            logging.error(f'Возврат юзеру {customer_id} денег {price}$. Ошибка: {e}')
            await refund_balance(customer_id, price)
        raise

async def voucher_text_loader(voucher):
    data = voucher.voucher
    v_data = data[0] if isinstance(data, list) else data
    serial = v_data.get('serialNumber') or '🧾 Отсутствует'
    pin = v_data.get('pin') or '❌ Ошибка кода'
    expiry = v_data.get('expiration') or '♾ Безлимит'
    return (
        f"<b>🎉 Поздравляем с покупкой!</b>\n"
        f"————————————————\n"
        f"🛍 <b>Товар:</b> <code>{voucher.voucher_name}</code>\n"
        f"🔑 <b>Код активации:</b>\n\n"
        f"<code>{pin}</code>\n\n"
        f"————————————————\n"
        f"📋 <b>S/N:</b> <code>{serial}</code>\n"
        f"⏳ <b>Годен до:</b> <i>{expiry}</i>\n"
        f"————————————————\n\n"
        f"<b>💡 Инструкция:</b> Введите код в приложении или на сайте сервиса. "
        f"Если будут проблемы - пиши в поддержку!"
    )

async def current_voucher_text_loader(voucher_id):
    voucher = await get_current_voucher(voucher_id)
    if voucher is None:
        raise BotError('Произошла ошибка, попробуйте снова.')
    data = voucher.voucher
    voucher_info = data[0] if isinstance(data, list) else data
    serial = voucher_info.get('serialNumber') or '🧾 Отсутствует'
    pin = voucher_info.get('pin') or '❌ Ошибка кода'
    expiry = voucher_info.get('expiration') or '♾ Безлимит'
    return(
        f"🛍 <b>Товар:</b> <code>{voucher.voucher_name}</code>\n"
        f"🔑 <b>Код активации:</b>\n\n"
        f"<code>{pin}</code>\n\n"
        f"————————————————\n"
        f"📋 <b>S/N:</b> <code>{serial}</code>\n"
        f"⏳ <b>Годен до:</b> <i>{expiry}</i>\n"
        f"————————————————\n\n"
        f"<b>💡 Инструкция:</b> Введите код в приложении или на сайте сервиса. "
        f"Если будут проблемы - пиши в поддержку!"
    )