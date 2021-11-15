
from flask_admin.contrib.sqla import ModelView
from flask_admin import expose
from flask_admin.actions import action
from flask import flash
from sqlalchemy.sql.expression import text
from . import db
from .models import UnknownStatement


class UnknownStatementView(ModelView):
    can_create = False
    
    @action('train_unknown', 'Train', 'Are you sure you want to train selected sentences(s)?')
    def action_recalculate(self, ids):
        from chatbot.bot import Sonny
        from chatterbot.ext.sqlalchemy_app.models import Statement
        count = 0
        for _id in ids:
            # Do some work with the id, e.g. call a service method
            learningSentence = UnknownStatement.query.filter_by(id = _id).first()
            if not learningSentence.answer:
                continue
            question = Statement(text = learningSentence.question)
            answer = Statement(text = learningSentence.answer)
            answer.in_response_to = learningSentence.question
            Sonny.storage.create_many([question, answer])
            db.session.delete(learningSentence)
            db.session.commit()
            count += 1
        flash("{0} sentences (s) charges is trained".format(count))