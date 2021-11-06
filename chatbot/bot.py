from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.response_selection import get_first_response
from chatbot.sentence_similarity import VietnameseJaccardSimilarity, VietnameseCosineSimilarity
import numpy as np

DEFAULT_REPONSE = 'Xin lỗi, mình chưa được huấn luyện về vấn đề bạn vừa nói.'
NOT_VIETNAMESE_LANGUAGE_REPONSE = 'Xin lỗi, mình chỉ hiểu tiếng việt. Sorry i can only understand vietnamese.'

TAG_REMOVE = ('CH', 'Np', 'C', 'Cc', 'M')
with open('chatbot/vietnamese_stopwords.txt', 'r', encoding="utf8") as f:
    STOPWORDS = np.array(f.read().split('\n'))

Sonny = ChatBot("Sonny",
    storage_adapter='chatbot.storage_adapter.MySQLStorageAdapter',
    read_only = True,
    statement_comparison_function=VietnameseCosineSimilarity,
    logic_adapters=[
            {
                'import_path': 'chatterbot.logic.BestMatch',
                'default_response': DEFAULT_REPONSE,
                'maximum_similarity_threshold': 0.75,
                "response_selection_method": get_first_response
            }
        ],
    database_uri='sqlite:///database.db')


def __train__():
    trainer = ChatterBotCorpusTrainer(Sonny)
    trainer.train("chatbot/corpus")



