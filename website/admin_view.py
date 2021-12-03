
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin import expose, BaseView, AdminIndexView
from flask_admin.actions import action
from flask import flash, redirect, url_for, session, request
from flask_login.utils import login_user
from sqlalchemy.sql.expression import column, text
from sqlalchemy.sql.functions import user
from . import db
from .models import User, Role
from chatbot.models import Statement, Tag, UnknownStatement
import os.path as op
import yaml
from definition import ROOT_PATH
from chatbot.bot import Sonny
from chatbot import bot
from flask_login import current_user, logout_user, login_user, login_required
from .form import LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
from chatbot.tag import VietnameseTager


# Create customized index view class that handles login & registration
class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if current_user.is_authenticated and session.get('user_role', None) == Role.ADMIN.value:
            return self.render('admin/dashboard.html')
        return redirect(url_for('admin.login'))

    @expose('/login', methods=['GET', 'POST'])
    def login(self):
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.role == Role.ADMIN:
                if check_password_hash(user.password, form.password.data):
                    flash('Đăng nhập thành công', category='success')
                    session['user_role'] = user.role.value
                    login_user(user, remember=True,
                               duration=timedelta(hours=1))
                    return redirect(url_for('admin.index'))
                else:
                    flash("Sai mật khẩu", category='error')
            else:
                flash("Tài khoản không tồn tại", category='error')
        return self.render('admin/login_user.html', form=form)

    @expose('/logout/')
    @login_required
    def logout(self):
        session['user_role'] = None
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

    column_list = ('question', 'answer', 'tag', 'create_at')
    form_edit_rules = ('question', 'answer', 'tag')
    column_labels = {'question': 'người dùng hỏi',
                     'answer': 'chatbot trả lời',
                     'create_at': 'thời điểm hỏi',
                     'tag': 'ngữ cảnh'}

    column_searchable_list = ['question']
    column_filters = ['tag']

    @action('train_unknown', 'Train', 'Train chatbot với những câu đã chọn?')
    def action_train(self, ids):
        count = 0
        for _id in ids:
            # Do some work with the id, e.g. call a service method
            learningSentence = UnknownStatement.query.filter_by(id=_id).first()
            if not learningSentence.answer:
                continue
            question = Statement(text=learningSentence.question)
            answer = Statement(text=learningSentence.answer)
            answer.in_response_to = learningSentence.question
            Sonny.storage.create_many([question, answer])
            db.session.delete(learningSentence)
            db.session.commit()
            count += 1
        flash("{0} câu (s) đã được train thành công".format(count))


class BotTrainFileView(FileAdmin):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.role == Role.ADMIN:
            return True
        return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin.index'))

    can_delete = False
    can_edit = True

    @action('train_file', 'Train', 'Bạn có chắc là train chatbot với mấy file (s) đã chọn?')
    def action_train_file(self, ids):

        dir_path = op.join(ROOT_PATH, 'chatbot/corpus')
        count = 0
        for _id in ids:
            # Do some work with the id, e.g. call a service method
            file_path = dir_path + '/' + _id
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                tag = data['categories']

                # Remove already learning tags
                (db.session.query(Statement)
                    .join(Statement.tags)
                    .filter(Tag.name == tag)
                 ).delete()
                db.session.commit()

                # Train file again
                bot.__train__(filePath=file_path)

            count += 1
        flash("{0} file (s) charges is trained".format(count))


class RelearnView(MyModelView):
    can_delete = False

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
    column_list = ('in_response_to', 'text', 'tags', 'created_at')
    form_edit_rules = ('in_response_to', 'text', 'tags')
    form_create_rules = ('in_response_to', 'text', 'tags')
    column_labels = dict(in_response_to='Người dùng hỏi',
                         text='Chatbot trả lời', tags='Ngữ cảnh', created_at='Thời điểm tạo')

    column_searchable_list = ['in_response_to', 'text']
    column_filters = ['tags']

    def __init__(self, model, session, name=None, category=None, endpoint=None, url=None, static_folder=None, menu_class_name=None, menu_icon_type=None, menu_icon_value=None):
        super().__init__(model, session, name=name, category=category, endpoint=endpoint, url=url, static_folder=static_folder,
                         menu_class_name=menu_class_name, menu_icon_type=menu_icon_type, menu_icon_value=menu_icon_value)
        self.tagger = VietnameseTager()

    def delete_model(self, model):
        try:
            self.on_model_delete(model)
            question_statement = (db.session.query(Statement)
                                  .filter_by(id=model.id-1).first())

            self.session.flush()
            self.session.delete(model)
            self.session.delete(question_statement)
            self.session.commit()
        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash('Failed to delete record. %(error)s', category='error')

            self.session.rollback()

            return False
        else:
            self.after_model_delete(model)

        return True

    def update_model(self, form, model):
        """
            Update model from form.

            :param form:
                Form instance
            :param model:
                Model instance
        """
        try:
            form.populate_obj(model)
            # Update question statement
            question_statement = (db.session.query(Statement)
                                  .filter_by(id=model.id-1).first())
            question_statement.text = model.in_response_to
            search_text = self.tagging(model.in_response_to)
            question_statement.search_text = search_text

            # Update answer statement
            model.search_text = self.tagging(model.text)
            model.search_in_response_to = search_text

            self._on_model_change(form, model, False)
            self.session.commit()
        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash('Failed to update record. %(error)s',
                      error=str(ex), category='error')

            self.session.rollback()

            return False
        else:
            self.after_model_change(form, model, False)

        return True

    def create_model(self, form):
        """
            Create model from form.

            :param form:
                Form instance
        """
        try:
            model = self.build_new_instance()

            form.populate_obj(model)

            # Create question statement
            question_statement = Statement(text=model.in_response_to)
            search_text = self.tagging(model.in_response_to)
            question_statement.search_text = search_text

            # Update answer statement
            model.search_text = self.tagging(model.text)
            model.search_in_response_to = search_text

            self.session.add(question_statement)
            self.session.add(model)
            self._on_model_change(form, model, True)
            self.session.commit()
        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash('Failed to create record. %(error)s',
                      error=str(ex), category='error')

            self.session.rollback()

            return False
        else:
            self.after_model_change(form, model, True)

        return model

    def get_query(self):
        return super(MyStatementView, self).get_query().filter(Statement.in_response_to != None)

    def tagging(self, text):
        return self.tagger.get_bigram_pair_string(text)
