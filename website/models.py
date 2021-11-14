from chatterbot import constants
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from . import db
from chatterbot.ext.sqlalchemy_app.models import Statement, Tag

class Base(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    
class UnknownStatement(Base):
    __tablename__ = 'unknowstatement'
    question = db.Column(db.String(2000), nullable=False)
    answer = db.Column(db.String(2000))
    create_at = db.Column(db.DateTime(timezone=True), default=func.now())
    isTrain = db.Column(db.Boolean(), default=False)
    
    def __repr__(self) -> str:
        return f'<UnknowStatement {self.question}>'    