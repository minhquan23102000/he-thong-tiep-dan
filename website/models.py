from enum import Enum, auto
from chatterbot import constants
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from . import db
from chatbot.models import Statement, Tag
from flask_login import UserMixin
