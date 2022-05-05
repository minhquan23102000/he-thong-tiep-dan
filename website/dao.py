import random
from typing import List

from chatbot.models import Conversation, Question, Statement, Tag
from flask import session
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func

from website import db


def get_chat_history(conversation_id, topn=10):
    if conversation_id == None or topn <= 0:
        return {}

    questions = (
        db.session.query(Question)
        .filter(Question.conversation_id == conversation_id)
        .order_by(Question.id.desc())
        .limit(topn)
    )
    result = {}
    result = {"chat_history": []}

    for q in questions[::-1]:
        chat = dict()
        chat["question"] = q.asking
        chat["answer"] = q.answer
        result["chat_history"].append(chat)

    conversation = (
        db.session.query(Conversation)
        .filter(Conversation.id == conversation_id)
        .first()
    )

    for q in questions:
        if q.statement != None:
            break

    if q.statement and q.statement.get_tags() not in ["lời chào", "cảm xúc", None]:
        result[
            "guide"
        ] = f"Xin chào {conversation.person_name}, bạn cần mình giúp gì về thủ tục {q.statement.get_tags()}?"
        result["next_questions"] = q.statement.get_next_questions()
        result["tag"] = q.statement.get_tags()
    else:
        result["guide"] = f"Xin chào {conversation.person_name}!"
        result["next_questions"] = []
        result["tag"] = "none"

    return result


def new_conversation():
    conversation = Conversation()
    if current_user.is_authenticated:
        conversation.user_id = current_user.id
    db.session.add(conversation)
    db.session.commit()
    db.session.flush()
    return conversation

def get_recommend_questions(tag="none", n = 3) -> List[str]:
    if tag=='none':
        return ['Làm giấy khai sinh như thế nào?', 'Hỗ trợ đăng ký kết hôn', 'Làm giấy thường trú']
    
    
    recommend_questions = []
    statement = db.session.query(Statement).filter(Tag.name == tag).order_by(func.random()).limit(3)
    
    for statement in statement:
        recommend_questions.append(statement.in_response_to)
    
    return recommend_questions

def get_conversation_id():
    return session.get("conversation_id")


def get_database() -> SQLAlchemy:
    return db
