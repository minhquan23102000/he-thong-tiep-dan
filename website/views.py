from flask import Blueprint, render_template, request, flash, request, Response
import requests
from chatbot import bot
from . import db
from .models import UnknownStatement    
from . import config
import json
from pymessager.message import Messager


client = Messager(config.FB_PAGE_ACCESS_TOKEN)
views = Blueprint('views', __name__)
Sonny = bot.Sonny
 

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/get')
def get_bot_response():    
    userText = request.args.get('msg')
    return chatbot_reponse(str(userText))

  

def chatbot_reponse(msg: str):
    #Get reponse from bot
    reponse = Sonny.get_response(msg)
    if reponse.confidence <= 0.1:
        reponse = bot.DEFAULT_REPONSE
    else:
        reponse = reponse.text
   

    #Google search this paper if bot does not know about it
    flag_words = ['thủ tục', 'hành chính', 'giấy tờ', 'đơn', 'giấy phép', 'đăng ký', 'văn bản', 'biên bản']
    if reponse == bot.DEFAULT_REPONSE:
        from pyvi import ViTokenizer
        words = ViTokenizer.tokenize(msg)
        if any(w.replace('_', ' ').lower() in flag_words for w in words.split(' ')):
            from googlesearch import search
            # Make a request to google search
            try:
                url = list(search(msg, tld='com', lang='vi', num=1, stop=1, pause=2, country='vi'))[0]
                reponse = f'{bot.DEFAULT_REPONSE} Nhưng mình nghĩ bạn có thể tham khảo thêm tại đây: {url}'
            except Exception as e:
                reponse = bot.DEFAULT_REPONSE

    #Get random choice for default reponse
    if reponse == bot.DEFAULT_REPONSE:
        #Store question to database if bot has not learned it yet
        unknownStatement = UnknownStatement(question=msg)
        db.session.add(unknownStatement)
        db.session.commit()
        #Get unknown reponse
        reponse = bot.get_unknow_reponse()

    return reponse

# Step up webhook for fb chat messenger
@views.route('/webhook', methods=["GET"])
def fb_webhook():
    verify_token = request.args.get('hub.verify_token')
    if verify_token == config.VERIFY_TOKEN:
        print("Verify sucess")
        return request.args.get('hub.challenge')
    return "Verify Failed"

@views.route('/webhook', methods=['POST'])
def fb_receive_message():
    message_entries = json.loads(request.data.decode('utf8'))['entry']
    for entry in message_entries:
        for message in entry['messaging']:
            if message.get('message'):
                print("{sender[id]} says {message[text]}".format(**message))
                user_message = message['message']['text']
                user_id = message['sender']['id']
                reponse = get_bot_response(user_message)
                client.send_text(user_id, reponse)
    return "Hi"


# @views.route('/webhook', methods=['GET'])
# def webhook_verify():
#     if request.args.get('hub.verify_token') == config.VERIFY_TOKEN:
#         return request.args.get('hub.challenge')
#     return "Wrong verify token"

# @views.route('/webhook', methods=['POST'])
# def webhook_action():
#     data = json.loads(request.data.decode('utf-8'))
#     for entry in data['entry']:
#             user_message = entry['messaging'][0]['message']['text']
#             user_id = entry['messaging'][0]['sender']['id']
#             response = {
#                 'recipient': {'id': user_id},
#                 'message': {}
#             }
#             response['message']['text'] = handle_message(user_id, user_message)
#             r = requests.post(
#                 'https://graph.facebook.com/v12.0/me/messages/?access_token=' + config.FB_PAGE_ACCESS_TOKEN, json=response)
#     #return Response(response="EVENT RECEIVED",status=200)
#     return r


# @views.route('/webhook_dev', methods=['POST'])
# def webhook_dev():
#     # custom route for local development
#     data = json.loads(request.data.decode('utf-8'))
#     user_message = data['entry'][0]['messaging'][0]['message']['text']
#     user_id = data['entry'][0]['messaging'][0]['sender']['id']
#     response = {
#         'recipient': {'id': user_id},
#         'message': {'text': handle_message(user_id, user_message)}
#     }
#     return Response(
#         response=json.dumps(response),
#         status=200,
#         mimetype='application/json'
#     )
