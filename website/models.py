from enum import Enum, auto
from chatterbot import constants
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from . import db
from chatbot.models import Statement, Tag
from flask_login import UserMixin

     
    
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
    
    