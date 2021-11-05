from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.response_selection import get_first_response
from chatterbot import languages

DEFAULT_REPONSE = 'Xin lỗi, mình chưa được huấn luyện về vấn đề bạn vừa nói.'
NOT_VIETNAMESE_LANGUAGE_REPONSE = 'Xin lỗi, mình chỉ hiểu tiếng việt. Sorry i can only understand vietnamese.'

Sonny = ChatBot("Sonny",
    storage_adapter='chatbot.storage_adapter.MySQLStorageAdapter',
    read_only = True,
    logic_adapters=[
            {
                'import_path': 'chatterbot.logic.BestMatch',
                'default_response': DEFAULT_REPONSE,
                'maximum_similarity_threshold': 1,
                "response_selection_method": get_first_response
            },
        ],
    database_uri='sqlite:///database.db')


def __train__():
    trainer = ChatterBotCorpusTrainer(Sonny)
    trainer.train("chatbot/corpus")


   