from src.models import User


def get_user(uid: int) -> User:
    if User.select().where(User.id == uid).exists():
        # User exists, return data
        return User.get(User.id == uid)

    # User doesn't exist, create one
    user = User.create(id=uid)
    return user
