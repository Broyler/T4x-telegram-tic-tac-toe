from src.models import Invitation


def create_invitation(inviter_id: int, acceptor_id: int) -> Invitation:
    return Invitation.create(inviter_id=inviter_id, acceptor_id=acceptor_id)
