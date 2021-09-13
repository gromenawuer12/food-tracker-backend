from flask import Flask
import inject
from users.domain.user_database import UserDatabase
from units.domain.unit_database import UnitDatabase
from users.infrastructure.database.user_dynamodb import UserDynamoDB
from units.infrastructure.database.unit_dynamodb import UnitDynamoDB

def configure_inject(app: Flask) -> None:
    def config(binder: inject.Binder) -> None:
        binder.bind(UserDatabase, UserDynamoDB())
        binder.bind(UnitDatabase, UnitDynamoDB())

    inject.configure(config)