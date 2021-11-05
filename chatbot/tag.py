from chatterbot import languages
import string
from chatterbot.comparisons import Comparator
from chatbot import bot

class VietnameseTager(object):
    def __init__(self):
        import underthesea
        import numpy as np

        self.language = languages.VIE

        self.punctuation_table = str.maketrans(dict.fromkeys(string.punctuation))

        self.nlp = underthesea.pos_tag

        self.tag_remove = bot.TAG_REMOVE
       
        self.stopwords = bot.STOPWORDS

    def get_text_index_string(self, text):
        """
        Return a string of text containing part-of-speech, lemma pairs.
        """
        bigram_pairs = []

        if len(text) <= 2:
            text_without_punctuation = text.translate(self.punctuation_table)
            if len(text_without_punctuation) >= 1:
                text = text_without_punctuation

        document = self.nlp(text)

        for token in document:
            word = token[0].lower()
            tag = token[1]
            if word not in self.stopwords and tag not in self.tag_remove or word == 'Sonny':
                bigram_pairs.append('{}:{}'.format(
                        tag,
                        word
                    ))

        if not bigram_pairs:
            for token in document:
                word = token[0].lower()
                tag = token[1]
                if tag not in self.tag_remove:
                    bigram_pairs.append('{}:{}'.format(
                            tag,
                            word
                        ))

        return ' '.join(bigram_pairs)



class VietnameseJaccardSimilarity(Comparator):
    """
    Calculates the similarity of two statements based on the Jaccard index.
    The Jaccard index is composed of a numerator and denominator.
    In the numerator, we count the number of items that are shared between the sets.
    In the denominator, we count the total number of items across both sets.
    Let's say we define sentences to be equivalent if 50% or more of their tokens are equivalent.
    Here are two sample sentences:
        The young cat is hungry.
        The cat is very hungry.
    When we parse these sentences to remove stopwords, we end up with the following two sets:
        {young, cat, hungry}
        {cat, very, hungry}
    In our example above, our intersection is {cat, hungry}, which has count of two.
    The union of the sets is {young, cat, very, hungry}, which has a count of four.
    Therefore, our `Jaccard similarity index`_ is two divided by four, or 50%.
    Given our similarity threshold above, we would consider this to be a match.
    .. _`Jaccard similarity index`: https://en.wikipedia.org/wiki/Jaccard_index
    """
    
    def __init__(self, language):
        from underthesea import pos_tag
        import numpy as np
        super().__init__(language)

        self.nlp = pos_tag

        self.tag_remove = bot.TAG_REMOVE

        self.stopwords = bot.STOPWORDS

    def compare(self, statement_a, statement_b):
        """
        Return the calculated similarity of two
        statements based on the Jaccard index.
        """
        statement_a_lemmas = set(self.lemmaStatement(statement_a.text.lower()))
        statement_b_lemmas = set(self.lemmaStatement(statement_b.text.lower()))

        # Calculate Jaccard similarity
        numerator = len(statement_a_lemmas.intersection(statement_b_lemmas))
        denominator = float(len(statement_a_lemmas.union(statement_b_lemmas)))
        ratio = numerator / denominator
        return ratio

        

    def lemmaStatement(self, statement):
        words = []
        tags = []

        document = self.nlp(statement)

        for token in document:
            word = token[0]
            tag = token[1]
            if word not in self.stopwords and tag not in self.tag_remove or word == 'Sonny':
                words.append(word)
                tags.append(tag)

        if not words:
            for token in document:
                words.append(token[0])

        return words