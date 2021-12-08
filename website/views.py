from flask import Blueprint, render_template, request, flash, request, Response
import requests
from chatbot.bot import chatbot_reponse
from . import secret
import json
from flask import jsonify

views = Blueprint('views', __name__)


temp_db = {
    'khai sinh': [
        {'title': 'giấy chứng nhận kết hôn',
            'src': '/static/img/chung_nhan_ket_hon.jpg'},
        {'title': 'sổ thường trú', 'src': '/static/img/cm_noi_o.jpg'},
        {'title': 'giấy chứng sinh', 'src': '/static/img/giay_chung_sinh.jpg'},
        {'title': 'giấy tờ tùy thân', 'src': '/static/img/giay_tuy_than.jpg'},
        {'title': 'to_khai', 'src': '/static/img/to_khai_khai_sinh.jpg'}
    ],
    'đăng ký kết hôn': [
        {'title': 'giấy tờ tùy thân vợ/chồng ',
            'src': '/static/img/giay_tuy_than.jpg'},
        {'title': 'to_khai', 'src': '/static/img/to_khai_ket_hon.jpg'},
        {'title': 'giấy xác nhận tình trạng hôn nhân',
            'src': '/static/img/giay_xac_nhan_tinh_trang_hon_nhan.jpg'}
    ],
    'khai sinh lại': [
        {'title': 'giấy tờ tùy thân', 'src': '/static/img/giay_tuy_than.jpg'},
        {'title': 'to_khai', 'src': '/static/img/to_khai_khai_sinh_lai.jpg'},
        {'title': 'sổ thường trú', 'src': '/static/img/cm_noi_o.jpg'},
        {'title': 'bản sao khai sinh', 'src': '/static/img/trich_luc_khai_sinh.jpg'}
    ],
    'Đăng ký thường trú': [
        {'title': 'giấy tờ tùy thân', 'src': '/static/img/giay_tuy_than.jpg'},
        {'title': 'chứng minh nơi ở', 'src': '/static/img/cm_noi_o.jpg'},
        {'title': 'to_khai', 'src': '/static/img/to_khai_thuong_tru.jpg'}
    ]
}


@views.route('/')
def home():
    return render_template("index.html")


@views.route('/get')
def get_bot_response():
    userText = request.args.get('msg')
    oldtag = request.args.get('oldtag')

    reponse = chatbot_reponse(str(userText), oldtag)
    return jsonify(reponse)


@views.route('/get-img')
def get_img():
    tag = request.args.get('tag')
    try:
        data = temp_db[tag]
    except:
        data = {}
    return jsonify(data)

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
    data = {
        'recipient': {'id': user_id},
        'message': {}
    }
    data['message']['text'] = reponse
    requests.post(
        'https://graph.facebook.com/v12.0/me/messages/?access_token=' + secret.FB_PAGE_ACCESS_TOKEN, json=data)
