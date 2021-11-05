from chatbot.bot import Sonny
from chatterbot import constants
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from . import db



class MyStatement(db.Model, Sonny.storage.get_statement_model()):
    def __init__(self, *args, **kwargs):
        super(Sonny.storage.get_statement_model(), self).__init__(*args, **kwargs)

class MyTag(db.Model, Sonny.storage.get_tag_model()):
    pass
