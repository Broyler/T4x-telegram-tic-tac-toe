from datetime import datetime, UTC

from peewee import *

db = SqliteDatabase('database.db')


def utcnow():
    return datetime.now(UTC)


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    id = IntegerField(primary_key=True)
    wins = IntegerField(default=0)
    losses = IntegerField(default=0)
    ties = IntegerField(default=0)
    username = CharField(index=True, max_length=60)
    registered_date = DateTimeField(default=utcnow)


class Invitation(BaseModel):
    id = IntegerField(primary_key=True)
    inviter = ForeignKeyField(User, null=False)
    acceptor = ForeignKeyField(User, null=False)
    accepted_date = DateTimeField(default=utcnow)


class Admin(BaseModel):
    id = IntegerField(primary_key=True)
    user_id = ForeignKeyField(User)


class Game(BaseModel):
    id = IntegerField(primary_key=True)
    inviter = ForeignKeyField(User, null=False)
    acceptor = ForeignKeyField(User, null=True)
    is_accepted = BooleanField(default=False)
    created_date = DateTimeField(default=utcnow)


class Board(BaseModel):
    id = IntegerField(primary_key=True)
    game_id = ForeignKeyField(Game)
    inviters_move = BooleanField(default=True)
    board = FixedCharField(max_length=9, default="000000000")


db.connect()
db.create_tables([User, Game, Board, Admin, Invitation])
