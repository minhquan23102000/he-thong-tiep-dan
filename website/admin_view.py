import os.path as op
from datetime import timedelta

import chatbot
import yaml
from chatbot import Sonny
from chatbot.models import Conversation, Question, Role, Statement, Tag, User
from chatbot.tag import VietnameseTager
from definition import ROOT_PATH
from flask import flash, redirect, request, session, url_for
from flask_admin import AdminIndexView, BaseView, expose
from flask_admin.actions import action
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_required, login_user, logout_user
from flask_login.utils import login_user
from sqlalchemy.sql.expression import column, text
from sqlalchemy.sql.functions import user
from werkzeug.security import check_password_hash, generate_password_hash

from . import db
from .form import LoginForm


# Create customized index view class that handles login & registration
class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if current_user.is_authenticated and session.get(
                'user_role', None) == Role.ADMIN.value:
            return self.render('admin/dashboard.html')
        return redirect(url_for('admin.login'))

    @expose('/login', methods=['GET', 'POST'])
    def login(self):
        # Make sure that session will not be delete when close browser
        session.permanent = True
        attempt_login = session.get('attempt_login', 0)
        # If user login invalid five times in a rows. Lock this user for one hours
        if (attempt_login >= 5):
            return " Bạn đã bị khóa! Xin hãy quay lại trong vòng 1 tiếng nữa!!!"
        elif (attempt_login > 3):
            flash(
                f"Đăng nhập không thành công {session.get('attempt_login', 0)} lần. Lưu ý nếu quá năm lần bạn sẽ bị khóa trong một tiếng!!"
            )

        form = LoginForm()
        if form.validate_on_submit():
            user = db.session.query(User).filter_by(
                email=form.email.data).first()
            if user and user.role == Role.ADMIN:
                if check_password_hash(user.password, form.password.data):
                    flash('Đăng nhập thành công', category='success')
                    session['user_role'] = user.role.value
                    session['attempt_login'] = 0
                    login_user(user,
                               remember=True,
                               duration=timedelta(hours=1))
                    return redirect(url_for('admin.index'))
                else:
                    flash("Sai mật khẩu", category='error')
            else:
                flash("Tài khoản không tồn tại", category='error')
        session['attempt_login'] = attempt_login + 1
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

    column_list = ('asking', 'answer', 'tag', 'create_at',
                   'next_question_1', 'next_question_2', 'next_question_3')
    form_edit_rules = ('asking', 'answer', 'tag',
                       'next_question_1', 'next_question_2', 'next_question_3')
    column_labels = {
        'asking': 'người dùng hỏi',
        'answer': 'chatbot trả lời',
        'create_at': 'thời điểm hỏi',
        'tag': 'ngữ cảnh',
        'next_question_1': 'câu hỏi kế tiếp 1',
        'next_question_2': 'câu hỏi kế tiếp 2',
        'next_question_3': 'câu hỏi kế tiếp 3'
    }

    column_searchable_list = ['asking', 'answer']
    column_filters = ['tag']

    @action('train_unknown', 'Train', 'Train chatbot với những câu đã chọn?')
    def action_train(self, ids):
        count = 0
        for _id in ids:
            # Do some work with the id, e.g. call a service method
            learningSentence = db.session.query(Question).filter_by(
                id=_id).first()
            if not learningSentence.answer:
                continue

            statement = Statement(
                text=learningSentence.answer, in_response_to=learningSentence.asking)
            statement.add_next_question(learningSentence.get_next_questions())

            if learningSentence.tag:
                statement.add_tags(learningSentence.tag.name)

            learningSentence.is_not_known = False

            db.session.add(statement)
            db.session.commit()
            count += 1
        flash("{0} câu (s) đã được train thành công".format(count))

    def get_query(self):
        return super(UnknownStatementView,
                     self).get_query().filter(Question.is_not_known == True)


class RelearnView(MyModelView):
    can_delete = False
    form_columns = ('name', )

    edit_template = 'admin/relearn_model.html'

    @expose('/edit/')
    def edit_view(self):
        tag = request.args.get('id')
        children = (db.session.query(Statement).join(
            Statement.tags).filter(Tag.id == tag))

        self._template_args.update(
            dict(children=children,
                 edit_url=url_for('statement.edit_view', id=id)))

        return super(RelearnView, self).edit_view()


class MyStatementView(MyModelView):
    column_list = ('in_response_to', 'text', 'tags', 'created_at',
                   'next_question_1', 'next_question_2', 'next_question_3')
    form_edit_rules = ('in_response_to', 'text', 'tags',
                       'next_question_1', 'next_question_2', 'next_question_3')
    form_create_rules = ('in_response_to', 'text', 'tags',
                         'next_question_1', 'next_question_2', 'next_question_3')
    column_labels = dict(in_response_to='Người dùng hỏi',
                         text='Chatbot trả lời',
                         tags='Ngữ cảnh',
                         created_at='Thời điểm tạo',
                         next_question_1='Câu hỏi kế tiếp 1',
                         next_question_2='Câu hỏi kế tiếp 2',
                         next_question_3='Câu hỏi kế tiếp 3')

    column_searchable_list = ['in_response_to', 'text']
    column_filters = ['tags']

    def __init__(self,
                 model,
                 session,
                 name=None,
                 category=None,
                 endpoint=None,
                 url=None,
                 static_folder=None,
                 menu_class_name=None,
                 menu_icon_type=None,
                 menu_icon_value=None):
        super().__init__(model,
                         session,
                         name=name,
                         category=category,
                         endpoint=endpoint,
                         url=url,
                         static_folder=static_folder,
                         menu_class_name=menu_class_name,
                         menu_icon_type=menu_icon_type,
                         menu_icon_value=menu_icon_value)
        self.tagger = VietnameseTager()

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

            # Update answer statement
            model.search_text = self.tagging(model.text)
            model.search_in_response_to = self.tagging(model.in_response_to)

            self._on_model_change(form, model, False)
            self.session.commit()
        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash('Failed to update record. %(error)s',
                      error=str(ex),
                      category='error')

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
            # Update answer statement
            model.search_text = self.tagging(model.text)
            model.search_in_response_to = self.tagging(model.in_response_to)

            self.session.add(model)
            self._on_model_change(form, model, True)
            self.session.commit()
        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash('Failed to create record. %(error)s',
                      error=str(ex),
                      category='error')

            self.session.rollback()

            return False
        else:
            self.after_model_change(form, model, True)

        return model

    def tagging(self, text):
        return self.tagger.get_bigram_pair_string(text)
