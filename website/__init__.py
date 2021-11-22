from flask import Flask, request, make_response
from flask_restful import Resource, Api
import os.path as op
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from definition import ROOT_PATH
import numpy as np
import json

db = SQLAlchemy()

TAG_REMOVE = ('F', 'Np', 'C', 'M', 'L')
with open('chatbot/vietnamese_stopwords.txt', 'r', encoding="utf8") as f:
    STOPWORDS = np.array(f.read().split('\n'))

def create_app():
    #Init app
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    #Create database
    db.init_app(app)

    #Init api
    init_api(app)
    
   # Retrain chatbot  
   #from chatbot import bot  
    # check = ""
    # while (check != 'Y' and check != 'N'):
    #     check = input("Train lại chatbot? Y:N\n")
    #     if (check == "Y"):
    #         bot.Sonny.storage.drop()
    #         bot.__retrain__()


    #init_database(app)
    
    #User setting
    from .views import views
    app.register_blueprint(views, url_prefix='/')

    #Admin setting
    admin_setting(app)
    
    return app

def admin_setting(app):
    #Import model
    from .models import UnknownStatement
    from .admin_view import UnknownStatementView, BotTrainFileView
    #Admin setting
    admin = Admin(app, name = "Hệ thống tiếp dân thông minh", template_mode='bootstrap4')
    admin.add_view(UnknownStatementView(UnknownStatement, db.session, name='Unknown Sentences'))
    path = op.join(ROOT_PATH, 'chatbot/corpus')
    admin.add_view(BotTrainFileView(path, '/bot-train-data/', name='Bot Train Files'))
    


def init_database(app):
    #Import model
    from .models import UnknownStatement
    check = ""
    while (check != 'Y' and check != 'N'):
        check = input("tạo database? Y:N\n")
        if (check == "Y"):
            db.create_all(app=app)
            
            
def init_api(app):
    from chatbot import bot
    from chatbot.bot import chatbot_reponse
    
    api = Api(app)
    api.app.config['RESTFUL_JSON'] = {
        'ensure_ascii': False
    }
    class GetBotReponse(Resource):
        def get(self):
            message = request.form['message']
            reponse = {'reponse': chatbot_reponse(message)}
            return make_response(json.dumps(reponse))
        
    api.add_resource(GetBotReponse, '/get-reponse')