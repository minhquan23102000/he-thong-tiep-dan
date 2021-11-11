from flask import Flask
import os.path as op
from flask_admin import Admin
from flask_admin.contrib.fileadmin import FileAdmin
from flask_sqlalchemy import SQLAlchemy
import numpy as np

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

    

   # Retrain chatbot
    # from chatbot import bot
    # check = ""
    # while (check != 'Y' and check != 'N'):
    #     check = input("Train lại chatbot? Y:N\n")
    #     if (check == "Y"):
    #         bot.Sonny.storage.drop()
    #         bot.__train__()


    #User setting
    from .views import views
    app.register_blueprint(views, url_prefix='/')


    #Admin setting
    admin = Admin(app, name = "Hệ thống tiếp dân thông minh", template_mode='bootstrap4')
    path = op.join(op.dirname(app.instance_path), 'chatbot/corpus')
    admin.add_view(FileAdmin(path, '/bot-train-data/', name='Bot Train Files'))

    return app