from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.response_selection import get_random_response
from chatbot.sentence_similarity import VietnameseJaccardSimilarity, VietnameseCosineSimilarity
from website.config import SQLALCHEMY_DATABASE_URI

DEFAULT_REPONSE = 'Xin lỗi, mình chưa được huấn luyện về vấn đề bạn vừa nói.'
NOT_VIETNAMESE_LANGUAGE_REPONSE = 'Xin lỗi, mình chỉ hiểu tiếng việt. Sorry i can only understand vietnamese.'


Sonny = ChatBot("Sonny",
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


def __train__():
    trainer = ChatterBotCorpusTrainer(Sonny)
    trainer.train("chatbot/corpus")

def get_unknow_reponse():
    import random
    unknow_reponses = [DEFAULT_REPONSE, 'Xin lỗi, bạn có thể nói rõ hơn được không?', 'Xin lỗi, mình vẫn chưa học qua câu từ này :(']
    return random.choice(unknow_reponses)


