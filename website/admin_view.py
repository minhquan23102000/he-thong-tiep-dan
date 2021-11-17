
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin import expose
from flask_admin.actions import action
from flask import flash
from sqlalchemy.sql.expression import text
from . import db
from .models import UnknownStatement
import os.path as op
import yaml
from definition import ROOT_PATH
from chatbot.bot import Sonny
from chatbot import bot
from chatterbot.ext.sqlalchemy_app.models import Statement

class UnknownStatementView(ModelView):
    can_create = False
    
    @action('train_unknown', 'Train', 'Are you sure you want to train selected sentences(s)?')
    def action_train(self, ids):
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
        
class BotTrainFileView(FileAdmin):
    can_delete=False
    
    @action('train_file', 'Train', 'Are you sure you want to train selected file (s)?')
    def action_train_file(self, ids):

        dir_path = op.join(ROOT_PATH, 'chatbot/corpus')
        count = 0
        for _id in ids:
            # Do some work with the id, e.g. call a service method
            file_path = dir_path + '/' + _id
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                tag = data['categories']
                
                #Remove already learning tags
                # statements = tuple(Sonny.storage.filter(tags=tag))
                # for record in statements:
                #     print(record.text)
                #     Sonny.storage.remove(record.text)
                
                #Train file again
                bot.__train__(filePath=file_path)
                
            count += 1
        flash("{0} file (s) charges is trained".format(count))