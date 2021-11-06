from flask import Blueprint, render_template, request, flash
from chatbot import bot
import langid

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
    # #Check if not vietnamese langue
    # if langid.classify(msg)[0] != 'vi':
    #     return bot.NOT_VIETNAMESE_LANGUAGE_REPONSE

    #Get reponse from bot
    reponse = Sonny.get_response(msg)
    if reponse.confidence < 0.1:
        reponse = bot.DEFAULT_REPONSE
    else:
        reponse = reponse.text
   

    #Google search this paper if bot doesnt know about it
    flag_words = ['thủ tục', 'hành chính', 'giấy tờ', 'đơn', 'giấy phép', 'đăng ký', 'văn bản']
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
                print(e.__traceback__)

    return reponse
