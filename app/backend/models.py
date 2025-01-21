from uuid import uuid4
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.inspection import inspect


def get_uuid():
    return uuid4().hex


db = SQLAlchemy()


class Pub(db.Model):
    __tablename__ = "pubs"
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    name = db.Column(db.String(150), unique=True, nullable=False)
    address = db.Column(db.String(250), nullable=False)

    def get_as_dict(self):
        return {"id": self.id, "type": "pub", "attributes": {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs if c.key != "id"}}


class Group(db.Model):
    __tablename__ = "groups"
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    suggested_pub_id = db.Column(db.String(32), db.ForeignKey("pubs.id"))

    suggested_pub = db.relationship("Pub", backref="groups")

    def get_as_dict(self):
        return {
            "id": self.id,
            "type": "group",
            "attributes": {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs if c.key != "id"},
        }


class UserGroupQuery(db.Model):
    __tablename__ = "userGroupQuery"
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    user_id = db.Column(db.String(32), db.ForeignKey("users.id"), nullable=False)
    group_id = db.Column(db.String(32), db.ForeignKey("groups.id"), nullable=False)

    user = db.relationship("User", backref=db.backref("usergroupquery", lazy=True))
    group = db.relationship("Group", backref=db.backref("usergroupquery", lazy=True))

    def get_as_dict(self):
        return {
            "id": self.id,
            "type": "userGroupQuery",
            "attributes": {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs if c.key != "id"},
        }


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    address = db.Column(db.String(250), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    second_name = db.Column(db.String(150), nullable=False)

    def get_as_dict(self):
        return {
            "id": self.id,
            "type": "user",
            "attributes": {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs if c.key != "id"},
        }
