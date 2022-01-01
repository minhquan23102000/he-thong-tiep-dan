from chatterbot import conversation
from flask import Blueprint, render_template, request, flash, request, Response, session
import requests
from chatbot.bot import chatbot_reponse
from chatbot.models import *
from . import secret
import json
from flask import jsonify
from .constant.temp_db import make_img_guide
from flask_login import current_user
from website import db

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template("dichvucong.html")


@views.route('/get')
def get_bot_response():
    userText = request.args.get('msg')
    oldtag = request.args.get('oldtag')

    # Check if there are conversation in session, if not create a new conversation

    if session.get('conversation_id') == None:
        conversation = new_conversation()
        session['conversation_id'] = conversation.id

    reponse = chatbot_reponse(str(userText), oldtag,
                              session['conversation_id'])
    return jsonify(reponse)


@views.route('/get-img')
def get_img():
    tag = request.args.get('tag')
    try:
        data = make_img_guide(tag)
    except:
        data = {}
    return jsonify(data)


def new_conversation():
    conversation = Conversation()
    if current_user.is_authenticated:
        conversation.user_id = current_user.id
    db.session.add(conversation)
    db.session.commit()
    db.session.flush()
    return conversation


# =================================WEB HOOK DOWN HERE=============================================

# Step up webhook for fb chat messenger


@views.route('/webhook', methods=["GET"])
def fb_webhook():
    verify_token = request.args.get('hub.verify_token')
    if verify_token == secret.VERIFY_TOKEN:
        print("Verify sucess")
        return request.args.get('hub.challenge')
    return Response(response="Verified Failed", status=203)


@views.route('/webhook', methods=['POST'])
def fb_receive_message():
    message_entries = json.loads(request.data.decode('utf8'))['entry']
    for entry in message_entries:
        for message in entry['messaging']:
            if message.get('message'):
                print("{sender[id]} says {message[text]}".format(**message))
                user_message = message['message']['text']
                user_id = message['sender']['id']
                reponse = chatbot_reponse(user_message)
                send_reponse(reponse['response'], user_id)
                return Response(response="EVENT RECIEVED", status=200)
    return Response(response="NO MESSAGE", status=204)


def send_reponse(reponse: str, user_id):
    data = {'recipient': {'id': user_id}, 'message': {}}
    data['message']['text'] = reponse
    requests.post(
        'https://graph.facebook.com/v12.0/me/messages/?access_token=' +
        secret.FB_PAGE_ACCESS_TOKEN,
        json=data)
