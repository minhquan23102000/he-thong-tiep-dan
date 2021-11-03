from flask import Blueprint, render_template, request, flash
from chatbot import bot

views = Blueprint('views', __name__)
Sonny = bot.Sonny

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/get')
def get_bot_response():
    userText = request.args.get('msg')
    return str(Sonny.get_response(userText))