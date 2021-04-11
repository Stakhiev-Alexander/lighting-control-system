from .db import db


class User(db.Document):
    mac_hash = db.StringField(required=True, unique=True)
