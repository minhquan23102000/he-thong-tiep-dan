from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, UniqueConstraint, Enum, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declared_attr, declarative_base
import enum
from chatterbot.conversation import StatementMixin
from chatterbot import constants
from flask_login import UserMixin


class ModelBase(object):
    """
    An augmented base class for SqlAlchemy models.
    """
    @declared_attr
    def __tablename__(cls):
        """
        Return the lowercase class name as the name of the table.
        """
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True, autoincrement=True)


Base = declarative_base(cls=ModelBase)

tag_association_table = Table(
    'tag_association', Base.metadata,
    Column('tag_id', Integer, ForeignKey('tag.id')),
    Column('statement_id', Integer, ForeignKey('statement.id')),
    UniqueConstraint('tag_id', 'statement_id', name='Tag_Statement_Unique'))


class Tag(Base):
    """
    A tag that describes a statement.
    """

    name = Column(String(constants.TAG_NAME_MAX_LENGTH), unique=True)

    def __repr__(self):
        return '<Tag %r>' % (self.name)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class UnknownStatement(Base):
    question = Column(String(255), nullable=False)
    answer = Column(String(255))
    tag_id = Column(Integer(), ForeignKey('tag.id'))
    tag = relationship('Tag',
                       backref=backref('unknowstatements', lazy='dynamic'))
    create_at = Column(DateTime(timezone=True), default=func.now())

    def __repr__(self) -> str:
        return f'<UnknowStatement {self.question}>'


class Statement(Base, StatementMixin):
    """
    A Statement represents a sentence or phrase.
    """

    confidence = 0

    text = Column(String(constants.STATEMENT_TEXT_MAX_LENGTH))

    search_text = Column(String(constants.STATEMENT_TEXT_MAX_LENGTH),
                         nullable=False,
                         server_default='')

    conversation = Column(String(constants.CONVERSATION_LABEL_MAX_LENGTH),
                          nullable=False,
                          server_default='')

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    tags = relationship('Tag',
                        secondary=lambda: tag_association_table,
                        backref='statements')

    in_response_to = Column(String(constants.STATEMENT_TEXT_MAX_LENGTH),
                            nullable=True)

    search_in_response_to = Column(String(constants.STATEMENT_TEXT_MAX_LENGTH),
                                   nullable=False,
                                   server_default='')

    persona = Column(String(constants.PERSONA_MAX_LENGTH),
                     nullable=False,
                     server_default='')

    def get_tags(self):
        """
        Return a list of tags for this statement.
        """
        return [tag.name for tag in self.tags]

    def add_tags(self, *tags):
        """
        Add a list of strings to the statement as tags.
        """
        self.tags.extend([Tag(name=tag) for tag in tags])

    def __str__(self):
        return f'{self.text}: {self.in_response_to}'

    def __unicode__(self):
        return f'{self.text}: {self.in_response_to}'


class PaperType(enum.Enum):
    TOKHAI = enum.auto()
    GIAYTO = enum.auto()


class Paper(Base):
    paper_name = Column(String(250), unique=True)
    paper_description = Column(String(500))
    paper_type = Column(Enum(PaperType), nullable=False)


class Role(enum.Enum):
    ADMIN = enum.auto()
    PEOPLE = enum.auto()


class User(Base, UserMixin):
    email = Column(String(150), unique=True)
    password = Column(String(150))
    first_name = Column(String(150))
    last_name = Column(String(150))
    role = Column(Enum(Role), nullable=False)
    create_at = Column(DateTime(timezone=True), default=func.now())


class Sentiment(enum.Enum):
    HAILONG = enum.auto()
    KHONGHAILONG = enum.auto()


class Conversation(Base):
    user_id = Column(Integer(), ForeignKey('user.id'), nullable=True)
    create_at = Column(DateTime(timezone=True), default=func.now())
    sentiment = Column(Enum(Sentiment), nullable=True)
    question = relationship("Question", backref=backref("question"))


class Question(Base):
    conversation_id = Column(Integer(), ForeignKey(
        'conversation.id'), nullable=False)
    tag_id = Column(Integer(), ForeignKey('tag.id'), nullable=False)
    asking = Column(String(255), nullable=False)
    answer = Column(String(255), nullable=False)
    create_at = Column(DateTime(timezone=True), default=func.now())
    is_not_known = Column(Boolean(), default=False)
    tag = relationship('Tag',
                       backref=backref('questions', lazy='dynamic'))
