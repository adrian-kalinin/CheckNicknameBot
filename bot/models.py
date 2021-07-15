from peewee import Model, IntegerField, BooleanField

from settings import DEBUG

if not DEBUG:
    from peewee import PostgresqlDatabase
    from settings import (
        DB_NAME, DB_USER, DB_PASSWORD,
        DB_HOST, DB_PORT
    )

    database = PostgresqlDatabase(
        database=DB_NAME,
        user=DB_USER, password=DB_PASSWORD,
        host=DB_HOST, port=DB_PORT
    )

else:
    from peewee import SqliteDatabase
    from settings import SQLITE_DB_PATH

    database = SqliteDatabase(SQLITE_DB_PATH)


# base model for other models
class BaseModel(Model):
    class Meta:
        database = database


# model that represents user
class User(BaseModel):
    user_id = IntegerField(primary_key=True, unique=True)
    requests = IntegerField(default=0)
    active = BooleanField(default=True)
