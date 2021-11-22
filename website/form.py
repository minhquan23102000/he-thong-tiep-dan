from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from .models import User, Role

class LoginForm(FlaskForm):
    email  = StringField('Email', validators=[DataRequired("Email không thể bỏ trống")])
    password = PasswordField('Password', validators=[DataRequired("Mật khẩu không thể để trống")])
    submit = SubmitField('Đăng nhập')
    