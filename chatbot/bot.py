from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.response_selection import get_first_response
from chatterbot import languages

default_reponse = 'Mình thật lòng xin lỗi, mình vẫn chưa học câu bạn vừa nói. Nếu có thể, vui lòng bạn nói rõ hơn được không ạ?'

Sonny = ChatBot("Sonny",
    storage_adapter='chatbot.storage_adapter.MySQLStorageAdapter',
    read_only = True,
    logic_adapters=[
            {
                'import_path': 'chatterbot.logic.BestMatch',
                'default_response': default_reponse,
                'maximum_similarity_threshold': 1,
                "response_selection_method": get_first_response
            }
        ],
    database_uri='sqlite:///database.db')


def __train__():
    trainer = ChatterBotCorpusTrainer(Sonny)
    trainer.train("chatbot/corpus")


   