import json
import os.path as op
from functools import wraps

import numpy as np
from definition import ROOT_PATH
from flask import (Flask, flash, make_response, redirect, render_template,
                   request, url_for)
from flask_admin import Admin
from flask_login import LoginManager
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

TAG_REMOVE = ['F', 'Np', 'C', 'M', 'L', 'X']
with open('chatbot/vietnamese_stopwords.txt', 'r', encoding="utf8") as f:
    STOPWORDS = np.array(f.read().split('\n'))


def create_app():
    # Init app
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    # Connect db to app
    db.init_app(app)
    # Init database, only run it once or run when create new models
    # check = ""
    # while (check != "Y" and check != "N"):
    #     check = input("Tao lai database? Y:N")
    #     if (check == "Y"):
    #         init_database(app)


    # Init api
    init_api(app)

    # Init flask login
    init_login(app)

    # Retrain chatbot
    import chatbot

    from .constant import temp_db
    check = ""
    while (check != 'Y' and check != 'N'):
        check = input("Train lại chatbot? Y:N\n")
        if (check == "Y"):
            chatbot.Sonny.storage.drop()
            chatbot.__retrain__()
            with app.app_context():
                temp_db.insert_temp_db()

    # User setting
    from .views import views
    app.register_blueprint(views, url_prefix='/')
    from .auth import auth
    app.register_blueprint(auth, url_prefix='/')
    from .tokhai import tokhai
    app.register_blueprint(tokhai, url_prefix="/to-khai")

    # Admin setting
    admin_setting(app)

    return app


def admin_setting(app):
    # Import model
    from chatbot.models import Question, Statement, Tag

    from website.admin_view import MyModelView

    from .admin_view import (MyAdminIndexView, MyStatementView, RelearnView,
                             UnknownStatementView)

    # Admin setting
    admin = Admin(app,
                  name="Hệ thống quản lý dành cho cán bộ",
                  template_mode='bootstrap4',
                  index_view=MyAdminIndexView())

    # Unknow statement view, view store all message that the chatbot did not know
    admin.add_view(
        UnknownStatementView(Question,
                             db.session,
                             name='Các câu chưa học'))
    # Corpus manager view, we can add a new file corpus and train it
    # path = op.join(ROOT_PATH, 'chatbot/corpus')
    # admin.add_view(BotTrainFileView(path, '/bot-train-data/', name='Dữ liệu huấn luyện'))

    # RelearnView, view manager all the statements chatbot has learned.
    admin.add_view(RelearnView(Tag, db.session, name="Quản lý ngữ cảnh"))
    admin.add_view(
        MyStatementView(Statement,
                        db.session,
                        endpoint='statement',
                        name='Huấn luyện chatbot'))


def init_database(app):
    # Import model
    import chatbot
    import chatbot.models
    from chatbot.models import (Base, Conversation, Paper, PaperLinkTag,
                                Question, Role, Statement, Tag, User)

    chatbot.Sonny.storage.recreate_database()

    # Create test data for admin login
    from werkzeug.security import generate_password_hash
    admin_user = User(email='admin',
                      password=generate_password_hash("adminNCKH"),
                      last_name="admin",
                      role=Role.ADMIN)
    session = chatbot.Sonny.storage.get_session()
    session.add(admin_user)
    session.commit()
    session.close()


def init_api(app):
    from chatbot import chatbot_reponse

    api = Api(app)
    api.app.config['RESTFUL_JSON'] = {'ensure_ascii': False}

    class GetBotReponse(Resource):
        def get(self):
            message = request.form['message']
            reponse = chatbot_reponse(message)
            return make_response(json.dumps(reponse))

    api.add_resource(GetBotReponse, '/get-reponse')


def init_login(app):
    from chatbot.models import User
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return db.session.query(User).get(int(id))
