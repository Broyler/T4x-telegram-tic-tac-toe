from src.models import Invitation, Game
from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.fsm.state import default_state
from static import messages
from datetime import datetime

from src.users import get_user

router = Router()


def create_invitation(inviter_id: int, acceptor_id: int) -> Invitation:
    return Invitation.create(inviter_id=inviter_id, acceptor_id=acceptor_id)


def invites_list(inviter_id: int) -> list[Game]:
    games = Game.select().where(Game.inviter == inviter_id and Game.is_accepted == False)
    return list(games)


@router.message(Command("invites"), default_state)
async def cmd_invites(message: types.message):
    user, _ = get_user(message.from_user)
    invites = invites_list(user.id)
    out = ""
    for idx, invite in enumerate(invites):
        out += f"{idx + 1}. "
        if invite.acceptor:
            out += str(invite.acceptor)

        else:
            out += "Без получателя"

        dt = datetime.strptime(invite.created_date, "%Y-%m-%d %H:%M:%S.%f%z")
        out += f" - {dt.strftime('%d.%m, %H:%M')}\n"

    await message.answer(messages.invs_list.format(out))

