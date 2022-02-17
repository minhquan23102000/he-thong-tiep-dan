from enum import Enum, auto

from chatbot.models import Statement, Tag
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
