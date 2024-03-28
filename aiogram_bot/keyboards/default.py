from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram_bot.messages import messages

from aiogram_bot.utils import funcs


def generate_group_keyboard(group_dict):
    builder = InlineKeyboardBuilder()
    for count, group_name in enumerate(group_dict.keys()):
        if count % 2:
            builder.add(
                InlineKeyboardButton(
                    text=messages.USER_GROUP_DICT.get(group_name, group_name),
                    callback_data=group_name
                )
            )
        else:
            builder.row(
                InlineKeyboardButton(
                    text=messages.USER_GROUP_DICT.get(group_name, group_name),
                    callback_data=group_name
                )
            )
    return builder.as_markup()


def generate_user_keyboard(user_list, group_name):
    builder = InlineKeyboardBuilder()
    for count, user_name in enumerate(user_list):
        if count % 2:
            builder.add(
                InlineKeyboardButton(
                    text=f'{messages.USER_STATUS_STATE_EMOJI[funcs.AD_users.get_user_status(user_name)]} {user_name}',
                    callback_data=user_name
                )
            )
        else:
            builder.row(
                InlineKeyboardButton(
                    text=f'{messages.USER_STATUS_STATE_EMOJI[funcs.AD_users.get_user_status(user_name)]} {user_name}',
                    callback_data=user_name
                )
            )

    if any(map(lambda x: funcs.AD_users.user_dict[x], user_list)):
        builder.row(
            InlineKeyboardButton(
                text=messages.BAN_ALL_GROUP_USERS,
                callback_data=f'ban_group {group_name}'
            )
        )
    else:
        builder.row(
            InlineKeyboardButton(
                text=messages.UNBAN_ALL_GROUP_USERS,
                callback_data=f'unban_group {group_name}'
            )
        )

    builder.row(
        InlineKeyboardButton(
            text=messages.BACK_TO_GROUPS_MESSAGE,
            callback_data='start'
        )
    )
    return builder.as_markup()


def generate_user_info_keyboard(user_name, user_current_state):
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text=messages.USER_TURN_STATE.get(user_current_state, '🔴'),
            callback_data=f'{messages.CALLBACK_TURN_STATE[user_current_state]} {user_name}'
        )
    )
    builder.add(
        InlineKeyboardButton(
            text=messages.BACK_TO_USERS_MESSAGE,
            callback_data=funcs.AD_users.reverse_group_dict[user_name]
        )
    )
    return builder.as_markup()
