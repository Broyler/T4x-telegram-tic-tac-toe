from src.models import User


def get_user(uid: int) -> (User, bool):
    """
    Fetches a user by telegram user id.
    :param uid: Telegram user id.
    :return: User object and whether it was just created or not.
    """
    if User.select().where(User.id == uid).exists():
        # User exists, return data
        return User.get(User.id == uid), False

    # User doesn't exist, create one
    user = User.create(id=uid)
    return user, True
