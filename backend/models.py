#C:\flask_dev\flaskreact\models.py
from uuid import uuid4 
from flask_sqlalchemy import SQLAlchemy

def get_uuid():
    return uuid4().hex

db = SQLAlchemy()
   
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(11), primary_key=True, unique=True, default=get_uuid)
    name = db.Column(db.String(150), unique=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.Text, nullable=False)
    photo = db.Column(db.String(150), unique=True)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}