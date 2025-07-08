from src.models import User
from aiogram.types import User as AiogramUser


def get_user(user: AiogramUser) -> (User, bool):
    """
    Fetches a user by telegram user id, or creates one if it doesn't exist.
    :param user: Telegram user object.
    :return: User object and whether it was just created or not.
    """
    if User.select().where(User.id == user.id).exists():
        # User exists, return data
        data = User.get(User.id == user.id)
        if data.username != user.username:  # Update username if changed
            data.username = user.username
            data.save()
        return data, False

    # User doesn't exist, create one
    user = User.create(id=user.id, username=user.username)
    return user, True


def find_handle(text: str) -> str | None:
    if text.count(' ') >= 1:
        handle = text.split(' ')[1]
        if handle.startswith('@') and handle[1:].replace('_', '').isalnum():
            return handle


def get_user_by_handle(handle: str) -> User | None:
    query = User.select().where(User.username == handle)
    if query.exists() and query.count() == 1:
        return query.get()
