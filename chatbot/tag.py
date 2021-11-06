from chatterbot import languages
import string
from chatterbot.comparisons import Comparator
from website import STOPWORDS, TAG_REMOVE
from .preprocessor import clean_url

class VietnameseTager(object):
    def __init__(self):
        from pyvi import ViTokenizer, ViPosTagger

        self.language = languages.VIE

        self.punctuation_table = str.maketrans(dict.fromkeys(string.punctuation))

        self.postag = ViPosTagger.postagging

        self.tokenize = ViTokenizer.tokenize


        self.tag_remove = TAG_REMOVE
       
        self.stopwords = STOPWORDS

    def get_text_index_string(self, text):
        """
        Return a string of text containing part-of-speech, lemma pairs.
        """
        text = clean_url(text)
        bigram_pairs = []

        if len(text) <= 2:
            text_without_punctuation = text.translate(self.punctuation_table)
            if len(text_without_punctuation) >= 1:
                text = text_without_punctuation

        
        document = self.tokenize(text)
        document = self.postag(document)

        for word, tag in zip(document[0], document[1]):
            word = word.replace('_', ' ')
            if word not in self.stopwords and tag not in self.tag_remove or word == 'Sonny':
                bigram_pairs.append('{}:{}'.format(
                        tag,
                        word
                    ))

        if not bigram_pairs:
            for word, tag in zip(document[0], document[1]):
                word = word.replace('_', ' ')
                if tag not in self.tag_remove:
                    bigram_pairs.append('{}:{}'.format(
                            tag,
                            word
                        ))

        return ' '.join(bigram_pairs)



