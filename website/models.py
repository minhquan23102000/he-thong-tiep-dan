from enum import Enum, auto
from chatterbot import constants
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from . import db
from chatterbot.ext.sqlalchemy_app.models import Statement, Tag
from flask_login import UserMixin

    
    
class UnknownStatement(db.Model):
    __tablename__  = 'unknowstatement'
    id = db.Column(db.Integer(), primary_key= True)
    question = db.Column(db.String(2000), nullable=False)
    answer = db.Column(db.String(2000))
    create_at = db.Column(db.DateTime(timezone=True), default=func.now())
    isTrain = db.Column(db.Boolean(), default=False)
    
    def __repr__(self) -> str:
        return f'<UnknowStatement {self.question}>'    
    
class Role(Enum):
    ADMIN = auto()
    PEOPLE = auto()
    
class User(db.Model, UserMixin):
    __tablename__  = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    role = db.Column(db.Enum(Role), nullable=False)
    create_at = db.Column(db.DateTime(timezone=True), default=func.now())