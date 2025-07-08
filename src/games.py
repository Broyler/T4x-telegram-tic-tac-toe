from aiogram import Router, types
from aiogram.filters.command import CommandStart
from src import users

from static import messages

router = Router()


@router.message(CommandStart)
async def start(message: types.Message):
    user = users.get_user(message.from_user.id)

    if message.text.count(' ') >= 1:
        # Invited, referral
        game_id = message.text.split(' ')[1]
        if not game_id.isdigit():
            # Invalid game id
            await message.reply(messages.invalid_ref)
            return

        # Todo: check if game id is valid and exists in games DB.
        await message.reply(messages.welcome_ref)
        return

    # Start command
    await message.reply(messages.welcome)
