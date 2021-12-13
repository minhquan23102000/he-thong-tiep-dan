from flask import Flask, request, make_response, flash, redirect, url_for, render_template
from functools import wraps
from flask_restful import Resource, Api
import os.path as op
from flask_admin import Admin
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from definition import ROOT_PATH
import numpy as np
import json

db = SQLAlchemy()

TAG_REMOVE = ['F', 'Np', 'C', 'M', 'L']
with open('chatbot/vietnamese_stopwords.txt', 'r', encoding="utf8") as f:
    STOPWORDS = np.array(f.read().split('\n'))


def create_app():
    # Init app
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    # Connect db to app
    db.init_app(app)

    # Init database, only run it once or run when create new models
    # init_database(app)

    # Init api
    init_api(app)

    # Init flask login
    init_login(app)

    # Retrain chatbot
    #from chatbot import bot
    #check = ""
    #while (check != 'Y' and check != 'N'):
    #    check = input("Train lại chatbot? Y:N\n")
    #    if (check == "Y"):
    #        bot.Sonny.storage.drop()
    #        bot.__retrain__()

    # User setting
    from .views import views
    app.register_blueprint(views, url_prefix='/')

    # Admin setting
    admin_setting(app)

    return app


def admin_setting(app):
    # Import model
    from website.admin_view import MyModelView
    from .admin_view import UnknownStatementView, BotTrainFileView, MyAdminIndexView, RelearnView, MyStatementView
    from chatbot.models import Statement, Tag, UnknownStatement
    # Admin setting
    admin = Admin(app,
                  name="Hệ thống quản lý dành cho cán bộ",
                  template_mode='bootstrap4',
                  index_view=MyAdminIndexView())

    # Unknow statement view, view store all message that the chatbot did not know
    admin.add_view(
        UnknownStatementView(UnknownStatement,
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
    from .models import User, Role
    from chatbot.models import Statement, Tag, UnknownStatement
    with app.app_context():
        db.create_all(app=app)

    check = input("tạo test data cho tài khoản admin? Y:N\n")
    if (check == "Y"):
        from werkzeug.security import generate_password_hash
        with app.app_context():
            admin_user = User(email='admin',
                              password=generate_password_hash("adminNCKH"),
                              last_name="admin",
                              role=Role.ADMIN)
            db.session.add(admin_user)
            db.session.commit()


def init_api(app):
    from chatbot import bot
    from chatbot.bot import chatbot_reponse

    api = Api(app)
    api.app.config['RESTFUL_JSON'] = {'ensure_ascii': False}

    class GetBotReponse(Resource):
        def get(self):
            message = request.form['message']
            reponse = chatbot_reponse(message)
            return make_response(json.dumps(reponse))

    api.add_resource(GetBotReponse, '/get-reponse')


def init_login(app):
    from .models import User
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
