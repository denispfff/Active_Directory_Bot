from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardMarkup

from logger import file_logger
from aiogram_bot.keyboards.default import *

from aiogram_bot.utils.funcs import AD_users
from aiogram_bot.keyboards.default import *

router = Router()


@router.callback_query(lambda c: c.data == 'start')
async def process_group_list_callback(callback_query):
    file_logger.info(f"User @{callback_query.from_user.username} started the bot.")

    builder: InlineKeyboardMarkup = generate_group_keyboard(AD_users.group_dict)

    await callback_query.message.edit_text(text=messages.START_MESSAGE, reply_markup=builder)


@router.callback_query(lambda c: c.data in AD_users.group_dict.keys())
async def process_user_list_callback(callback_query: CallbackQuery):
    AD_users.renew()
    group_name = callback_query.data
    user_list = funcs.AD_users.group_dict.get(group_name, [])

    builder: InlineKeyboardMarkup = generate_user_keyboard(user_list, group_name)
    message_text = f'{messages.SELECT_USER_MESSAGE} {messages.USER_GROUP_DICT.get(group_name, group_name)}'

    await callback_query.message.edit_text(text=message_text, reply_markup=builder)


@router.callback_query(lambda c: c.data in AD_users.user_dict.keys())
async def process_user_info_callback(callback_query: CallbackQuery):
    user_name: str | None = callback_query.data
    user_current_state: bool = AD_users.user_dict.get(user_name, False)

    builder: InlineKeyboardMarkup = generate_user_info_keyboard(user_name, user_current_state)
    message_text = (
        f'{messages.USER_MESSAGE} {user_name}\n'
        f'{messages.USER_STATUS_MESSAGE} {messages.USER_STATUS_STATE_MESSAGE[AD_users.get_user_status(user_name)]}\n'
        f'{messages.USER_LAST_LOGON_MESSAGE}\n'
        f'{AD_users.get_last_logon_date(user_name)}'
    )

    await callback_query.message.edit_text(text=message_text, reply_markup=builder)


@router.callback_query(lambda c: 'disable' in c.data)
async def process_disable_user_callback(callback_query: CallbackQuery):
    user_name: str = callback_query.data.split()[1]

    file_logger.info(
        f"Пользователь с TG ID @{callback_query.from_user.username} заблокировал пользователя {user_name}.")

    AD_users.disable_AD_user(user_name)
    await callback_query.answer(text=messages.USER_STATUS_STATE_MESSAGE[0])

    user_current_state = AD_users.user_dict.get(user_name, False)

    print(AD_users.get_user_status(user_name))
    builder: InlineKeyboardMarkup = generate_user_info_keyboard(user_name, user_current_state)
    message_text = (
        f'{messages.USER_MESSAGE} {user_name}\n'
        f'{messages.USER_STATUS_MESSAGE} {messages.USER_STATUS_STATE_MESSAGE[AD_users.get_user_status(user_name)]}\n'
        f'{messages.USER_LAST_LOGON_MESSAGE}\n'
        f'{AD_users.get_last_logon_date(user_name)}'
    )

    await callback_query.message.edit_text(text=message_text, reply_markup=builder)


@router.callback_query(lambda c: 'enable' in c.data)
async def process_enable_user_callback(callback_query: CallbackQuery):
    user_name = callback_query.data.split()[1]

    file_logger.info(
        f"Пользователь с TG ID @{callback_query.from_user.username} разблокировал пользователя {user_name}.")

    AD_users.enable_AD_user(user_name)
    await callback_query.answer(text=messages.USER_STATUS_STATE_MESSAGE[2])

    user_current_state = AD_users.user_dict.get(user_name, False)

    builder: InlineKeyboardMarkup = generate_user_info_keyboard(user_name, user_current_state)
    message_text = (
        f'{messages.USER_MESSAGE} {user_name}\n'
        f'{messages.USER_STATUS_MESSAGE} {messages.USER_STATUS_STATE_MESSAGE[AD_users.get_user_status(user_name)]}\n'
        f'{messages.USER_LAST_LOGON_MESSAGE}\n'
        f'{AD_users.get_last_logon_date(user_name)}'
    )

    await callback_query.message.edit_text(text=message_text, reply_markup=builder)


@router.callback_query(lambda c: 'unban_group' in c.data)
async def process_unban_group_callback(callback_query: CallbackQuery):
    group_name = callback_query.data.split()[1]

    file_logger.info(f"Пользователь с TG ID @{callback_query.from_user.username} разблокировал группу {group_name}.")

    AD_users.enable_AD_group(group_name)

    user_list = AD_users.group_dict.get(group_name, [])

    builder: InlineKeyboardMarkup = generate_user_keyboard(user_list, group_name)
    message_text = f'{messages.SELECT_USER_MESSAGE} {messages.USER_GROUP_DICT.get(group_name, group_name)}'

    await callback_query.message.edit_text(text=message_text, reply_markup=builder)


@router.callback_query(lambda c: 'ban_group' in c.data)
async def process_ban_group_callback(callback_query: CallbackQuery):
    group_name = callback_query.data.split()[1]

    file_logger.info(f"Пользователь с TG ID @{callback_query.from_user.username} заблокировал группу {group_name}.")

    AD_users.disable_AD_group(group_name)

    user_list = AD_users.group_dict.get(group_name, [])

    builder: InlineKeyboardMarkup = generate_user_keyboard(user_list, group_name)
    message_text = f'{messages.SELECT_USER_MESSAGE} {messages.USER_GROUP_DICT.get(group_name, group_name)}'

    await callback_query.message.edit_text(text=message_text, reply_markup=builder)
