from aiogram import Router, types
from aiogram.filters.command import CommandStart, Command
from aiogram.fsm.context import FSMContext

from src import users, referrals
from src.models import Game
from src.fsm import TState
from static import messages

router = Router()
OPEN_INV_LIMIT = 15


def get_game(game_id: int) -> Game | None:
    query = Game.select().where(Game.id == game_id)
    if query.exists():
        return query.get()


def get_game_str(text: str) -> Game | None:
    game_id = text.split(' ')[1]
    if game_id.isdigit():
        return get_game(int(game_id))


def create_game(user_id: int) -> Game:
    return Game.create(inviter=user_id)


@router.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    user, just_created = users.get_user(message.from_user)

    if message.text.count(' ') >= 1: # Invited, referral
        game = get_game_str(message.text)
        if game is None or game.is_accepted:  # Checks if game id is valid and exists in games DB
            # Invalid game id
            return await message.answer(messages.invalid_ref.format(message.from_user.first_name))

        if game.inviter == user:
            return await message.answer(messages.self_invite)

        # Successful invitation
        if just_created:  # Create an Invitation object if user has just registered
            referrals.create_invitation(game.inviter, user.id)

        game.is_accepted = True
        game.acceptor = user
        game.save()
        user_state = await state.get_state()

        if user_state is not None:
            return await message.answer(messages.game_accepted)

        await state.set_state(TState.selecting_move)
        await message.answer(messages.welcome_ref.format(message.from_user.first_name))

        # Todo: send game board, etc
        return

    # Regular start command
    await message.answer(messages.welcome.format(message.from_user.first_name))


@router.message(Command("inv"))
async def invite(message: types.Message, state: FSMContext):
    users.get_user(message.from_user)
    handle = users.find_handle(message.text)

    if handle == '@' + message.from_user.username:
        return await message.answer(messages.self_invite)

    uid = message.from_user.id
    if (Game.select()
            .where((Game.is_accepted == False)
                   & (Game.inviter == uid)).count() >= OPEN_INV_LIMIT):
        return await message.answer(messages.open_inv_limit)

    game = create_game(uid)

    if not handle:  # invalid handle
        await message.answer(messages.basic_invite.format(game.id))

    else:
        searched = users.get_user_by_handle(handle)
        if searched is None:  # no such user (or multiple)
            await message.reply(messages.invalid_handle_invite)
            await message.answer(messages.basic_invite.format(game.id))

        else:  # found a player with such username
            # Todo: send an invite to a registered player, change states
            pass

    user_state = await state.get_state()

    if user_state is not None:
        return await message.answer(messages.game_created)

    await state.set_state(TState.selecting_move)
    await message.answer(messages.game_created_started)
    # Todo: send board etc
