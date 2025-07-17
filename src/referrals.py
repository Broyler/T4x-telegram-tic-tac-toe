from aiogram.fsm.context import FSMContext

from src.models import Invitation, Game
from aiogram import Router, types, F
from aiogram.filters.command import Command
from aiogram.fsm.state import default_state
from static import messages
from datetime import datetime

from src.fsm import TState
from src.users import get_user

router = Router()


def create_invitation(inviter_id: int, acceptor_id: int) -> Invitation:
    if not Invitation.filter(inviter_id=inviter_id, acceptor_id=acceptor_id).exists():
        return Invitation.create(inviter_id=inviter_id, acceptor_id=acceptor_id)
    return Invitation.get(inviter_id=inviter_id, acceptor_id=acceptor_id)


def invites_list(inviter_id: int) -> list[Game]:
    games = Game.select().where(Game.inviter == inviter_id and Game.is_accepted == False).order_by(Game.id)
    return list(games)


def get_inv_list_msg(invites):
    out = ""
    for idx, invite in enumerate(invites):
        out += f"{idx + 1}. "
        if invite.acceptor:
            out += str(invite.acceptor)

        else:
            out += "Без получателя"

        dt = datetime.strptime(invite.created_date, "%Y-%m-%d %H:%M:%S.%f%z")
        out += f" - {dt.strftime('%d.%m, %H:%M')}\n"
    return out


@router.message(Command("invites"), default_state)
async def cmd_invites(message: types.message, state: FSMContext):
    user, _ = get_user(message.from_user)
    invites = invites_list(user.id)

    if len(invites) == 0:
        return await message.answer(messages.no_invites_yet)

    out = get_inv_list_msg(invites)

    await state.set_state(TState.invites)
    await message.answer(messages.invs_list.format(out))


@router.message(Command("stop"), TState.invites)
async def stop_invites(message: types.message, state: FSMContext):
    await state.set_state(default_state)
    await message.answer(messages.normal_mode)


@router.message(TState.invites)
async def select_invite(message: types.message, state: FSMContext):
    user, _ = get_user(message.from_user)
    invites = invites_list(user.id)

    if len(invites) == 0:
        await state.set_state(default_state)
        return await message.answer(messages.no_invites_yet)

    if not message.text.isdigit():
        return await message.answer(messages.enter_digits_or_stop.format(len(invites)))

    selected = int(message.text)
    if selected > len(invites):
        return await message.answer(messages.invalid_inv_selected.format(len(invites)))

    invite = invites[selected - 1]
    #Game.select().where(Game.id == invite.id).delete()
    invite.delete_instance()
    invites = invites_list(user.id)

    if len(invites) == 0:
        await state.set_state(default_state)
        return await message.answer(messages.all_inv_deleted)

    out = get_inv_list_msg(invites)
    await message.answer(messages.inv_deleted)
    await message.answer(messages.invs_list.format(out))
