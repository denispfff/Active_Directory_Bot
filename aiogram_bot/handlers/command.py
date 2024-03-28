from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup

from logger import file_logger
from aiogram_bot.keyboards.default import generate_group_keyboard

from aiogram_bot.messages import messages
from aiogram_bot.utils.funcs import AD_users


router = Router()


@router.message(Command("start"))
async def process_group_list_message(message: Message):
    file_logger.info(f"User @{message.from_user.username} started the bot.")

    builder: InlineKeyboardMarkup = generate_group_keyboard(AD_users.group_dict)

    await message.delete()
    await message.answer(
        text=messages.START_MESSAGE,
        reply_markup=builder
    )
