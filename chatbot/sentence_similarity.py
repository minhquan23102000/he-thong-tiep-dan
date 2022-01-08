from lib.chatterbot.comparisons import Comparator


class VietnameseCosineSimilarity(Comparator):
    """
    Calculates the similarity of two statements based on the Cosine Similarity
    Step 1: We convert statement to tf-idf vector
    Step 2: Caculate similarity base on consine similarity 
    """

    def compare(self, statement_a, statement_b):
        """
        Return the calculated similarity of two
        statements based on the cosine similarity.
        """
        import numpy as np
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity

        # Caculate tfidf cosine similarity
        tfidf = TfidfVectorizer(token_pattern=r'\S+')
        content = [
            ' '.join(statement_a.search_in_response_to),
            ' '.join(statement_b.search_in_response_to)
        ]
        matrix = tfidf.fit_transform(content)
        confidence = cosine_similarity(matrix[0], matrix[1])[0][0]

        # If any statement has oldtags value, add 5% confidence to it
        if statement_a.get_tags() == statement_b.get_tags() and confidence < 0.95:
            confidence += 0.05

        return np.round(confidence, 4)
