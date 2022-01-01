from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from chatbot.models import User, Role


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
                        DataRequired(message="Email không thể bỏ trống")])
    password = PasswordField('Mật khẩu', validators=[
                             DataRequired(message="Mật khẩu không thể để trống")])
    submit = SubmitField('Đăng nhập')
