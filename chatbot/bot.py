from .mychatbot import MyChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.response_selection import get_random_response
from chatbot.sentence_similarity import VietnameseJaccardSimilarity, VietnameseCosineSimilarity
from website.config import SQLALCHEMY_DATABASE_URI
import json


DEFAULT_REPONSE = 'Xin lỗi, mình chưa được huấn luyện về vấn đề bạn vừa nói.'
NOT_VIETNAMESE_LANGUAGE_REPONSE = 'Xin lỗi, mình chỉ hiểu tiếng việt. Sorry i can only understand vietnamese.'


Sonny = MyChatBot("Sonny",
    storage_adapter='chatbot.storage_adapter.MySQLStorageAdapter',
    read_only = True,
    statement_comparison_function=VietnameseCosineSimilarity,
    logic_adapters=[
            {
                'import_path': 'chatbot.logic_adapter.MyBestMatch',
                'default_response': DEFAULT_REPONSE,
                "response_selection_method": get_random_response
            }
        ],
    database_uri=SQLALCHEMY_DATABASE_URI)


def __retrain__():
    trainer = ChatterBotCorpusTrainer(Sonny)
    trainer.train("chatbot/corpus")
    
def __train__(filePath):
    trainer = ChatterBotCorpusTrainer(Sonny)
    trainer.train(filePath)
    
def chatbot_reponse(msg: str):
    from website import db
    from website.models import UnknownStatement
    #Check message lem
    if len(msg) >=600:
        return {'response': '...', 'tag': 'None'}
    
    #Get reponse from bot
    reponse = Sonny.get_response(msg)
    tag = reponse.get_tags()
    if not tag:
        tag = "None"
    else:
        tag = tag[0]
    
    if reponse.confidence <= 0.2:
        reponse = DEFAULT_REPONSE
    else:
        reponse = reponse.text

    #Google search this paper if bot does not know about it
    flag_words = ['thủ tục', 'hành chính', 'giấy tờ', 'đơn', 'giấy phép', 'đăng ký', 'văn bản', 'biên bản']
    if reponse == DEFAULT_REPONSE:
        from pyvi import ViTokenizer
        words = ViTokenizer.tokenize(msg)
        if any(w.replace('_', ' ').lower() in flag_words for w in words.split(' ')):
            from googlesearch import search
            # Make a request to google search
            try:
                url = list(search(msg, tld='com', lang='vi', num=1, stop=1, pause=2, country='vi'))[0]
                reponse = f'{DEFAULT_REPONSE} Nhưng mình nghĩ bạn có thể tham khảo thêm tại đây: {url}'
            except Exception as e:
                reponse = DEFAULT_REPONSE

    #Get random choice for default reponse
    if reponse == DEFAULT_REPONSE:
        #Store question to database if bot has not learned it yet
        unknownStatement = UnknownStatement(question=msg)
        db.session.add(unknownStatement)
        db.session.commit()
        #Get unknown reponse
        reponse = get_unknow_reponse()

    response_data = {'response': reponse, 
                     'tag': tag}
    return response_data

def get_unknow_reponse():
    import random
    unknow_reponses = [DEFAULT_REPONSE, 'Xin lỗi, bạn có thể nói rõ hơn được không?', 'Xin lỗi, mình vẫn chưa học qua câu từ này :(']
    return random.choice(unknow_reponses)


