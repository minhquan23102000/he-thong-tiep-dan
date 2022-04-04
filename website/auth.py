
from flask import (Blueprint, Response, flash, jsonify, render_template,
                   request, session)
from flask_login import current_user

from website import db

auth = Blueprint('auth', __name__)


@auth.route("/dang-ky")
def dang_ky():
    return render_template("dangky.html")
