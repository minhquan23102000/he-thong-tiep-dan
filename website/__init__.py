from flask import Flask
import os.path as op
from flask_admin import Admin
from flask_admin.contrib.fileadmin import FileAdmin



def create_app():
    #Init app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "7561117fac624e9b392242aa5e1722a22c1fb5f94014e5a0920b24e66e63e365"

    #User setting
    from .views import views
    app.register_blueprint(views, url_prefix='/')


    #Admin setting
    admin = Admin(app, name = "Hệ thống tiếp dân thông minh", template_mode='bootstrap4')
    path = op.join(op.dirname(app.instance_path), 'chatbot/corpus')
    admin.add_view(FileAdmin(path, '/bot-train-data/', name='Bot Train Files'))

    return app