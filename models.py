from enum import unique
from mongoengine import Document, fields


def _to_pydantic(doc: Document) -> dict:
    data = doc.to_mongo()
    data.pop("_id")
    data["id"] = str(doc.id)
    return data


class User(Document):
    meta = {"collection": "users"}
    user_name = fields.StringField(unique=True)
    email = fields.StringField(unique=True)
    hashed_password = fields.StringField()
    is_active = fields.BooleanField(default=True)

    def pydantic(self):
        return _to_pydantic(self)


class Item(Document):
    meta = {"collection": "items"}

    title = fields.StringField()
    description = fields.StringField()
