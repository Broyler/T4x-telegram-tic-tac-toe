from datetime import datetime

from peewee import *

db = SqliteDatabase('users.db')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    id = IntegerField(primary_key=True)
    wins = IntegerField(default=0)
    losses = IntegerField(default=0)
    registered_date = DateTimeField(default=datetime.now)


class Admin(BaseModel):
    id = ForeignKeyField(User)


class Game(BaseModel):
    id = IntegerField(primary_key=True)
    inviter = ForeignKeyField(User, null=False)
    acceptor = ForeignKeyField(User, null=False)
    is_accepted = BooleanField(default=False)
    created_date = DateTimeField(default=datetime.now)


class Board(BaseModel):
    id = IntegerField(primary_key=True)
    game_id = ForeignKeyField(Game)
    inviters_move = BooleanField(default=True)
    board = FixedCharField(max_length=9, default="000000000")
