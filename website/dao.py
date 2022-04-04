from chatbot.models import Conversation, Question, Statement, Tag
<<<<<<< HEAD
from flask_login import current_user
=======
from flask import session
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy
>>>>>>> 3f1637fdd6ba2c8d9b669388a32b4e629d7a2c9d

from website import db


def get_chat_history(conversation_id, topn=10):
<<<<<<< HEAD
    if conversation_id == None or topn <= 0:
        return []
=======

    
    if conversation_id == None or topn <= 0:
        return {}
>>>>>>> 3f1637fdd6ba2c8d9b669388a32b4e629d7a2c9d

    questions = (
        db.session.query(Question)
        .filter(Question.conversation_id == conversation_id)
        .order_by(Question.id.desc())
        .limit(topn)
    )
<<<<<<< HEAD
    result = []
=======
    result = {}
    result = {'chat_history': []}
>>>>>>> 3f1637fdd6ba2c8d9b669388a32b4e629d7a2c9d

    for q in questions[::-1]:
        chat = dict()
        chat["question"] = q.asking
        chat["answer"] = q.answer
<<<<<<< HEAD
        result.append(chat)

=======
        result['chat_history'].append(chat)

    
    conversation = db.session.query(Conversation).filter(Conversation.id == conversation_id).first()
    
    for q in questions:
        if q.statement != None:
            break
    
    if q.statement and q.statement.get_tags() not in ['lời chào', 'cảm xúc', None]:
        result['guide'] = f"Xin chào {conversation.person_name}, bạn cần mình giúp gì về thủ tục {q.statement.get_tags()}?"
        result['next_questions'] = q.statement.get_next_questions()
        result['tag'] = q.statement.get_tags()
    else:
        result['guide'] = f"Xin chào {conversation.person_name}!"
        result['next_questions'] = []
        result['tag'] = 'none'
    
     
    
    
>>>>>>> 3f1637fdd6ba2c8d9b669388a32b4e629d7a2c9d
    return result


def new_conversation():
    conversation = Conversation()
    if current_user.is_authenticated:
        conversation.user_id = current_user.id
    db.session.add(conversation)
    db.session.commit()
    db.session.flush()
    return conversation
<<<<<<< HEAD
=======


def get_conversation_id():
    return session.get("conversation_id")


def get_database() -> SQLAlchemy:
    return db
>>>>>>> 3f1637fdd6ba2c8d9b669388a32b4e629d7a2c9d
