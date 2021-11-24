
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin import expose, BaseView, AdminIndexView
from flask_admin.actions import action
from flask import flash, redirect, url_for, session, request
from flask_login.utils import login_user
from sqlalchemy.sql.expression import column, text
from sqlalchemy.sql.functions import user
from . import db
from .models import UnknownStatement, User, Role
from chatterbot.ext.sqlalchemy_app.models import Statement, Tag
import os.path as op
import yaml
from definition import ROOT_PATH
from chatbot.bot import Sonny
from chatbot import bot
from chatterbot.ext.sqlalchemy_app.models import Statement
from flask_login import current_user, logout_user, login_user, login_required
from .form import LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta


# Create customized index view class that handles login & registration
class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if current_user.is_authenticated and session.get('user_role', None) == Role.ADMIN.value:
            return self.render('admin/dashboard.html')
        return redirect(url_for('admin.admin_login'))
        

    @expose('/login', methods=['GET','POST'])
    def admin_login(self):
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email = form.email.data).first()
            if user:
                if check_password_hash(user.password, form.password.data):
                    flash('Đăng nhập thành công', category='success')
                    session['user_role'] = user.role.value
                    login_user(user, remember=True, duration=timedelta(hours=1))
                    return redirect(url_for('admin.index'))
                else:
                    flash("Sai mật khẩu", category='error')
            else:
                flash("Tài khoản không tồn tại", category='error')
        return self.render('admin/login.html', form=form)


    @expose('/logout/')
    @login_required
    def logout_view(self):
        session.update('user_role', None)
        logout_user()
        return redirect(url_for('admin.index'))

   
class MyModelView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.role == Role.ADMIN:
            return True 
        return False
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin.index'))
    
   

class UnknownStatementView(MyModelView):
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
    def is_accessible(self):
        if current_user.is_authenticated and current_user.role == Role.ADMIN:
            return True 
        return False
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin.index'))
    
    
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
        
        
        
class RelearnView(MyModelView):
    can_create=False
    can_delete=False
    edit_template = 'admin/relearn_model.html'
    @expose('/edit/')
    def edit_view(self):
        tag = request.args.get('id')
        children = (db.session.query(Statement)
                    .join(Statement.tags)
                    .filter(Tag.id == tag)
                    )
        
        self._template_args.update(dict(children=children,
                                        edit_url=url_for('statement.edit_view', id=id)))

        return super(RelearnView, self).edit_view()
    
class MyStatementView(MyModelView):
    column_list = ('in_response_to', 'text', 'tags')
    form_edit_rules  = ('in_response_to', 'text', 'tags')
    column_labels = dict(in_response_to = 'question', text = 'answer')