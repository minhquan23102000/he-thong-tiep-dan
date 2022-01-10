from lib.chatterbot.conversation import Statement


class IndexedTextSearch:
    """
    :param statement_comparison_function: The dot-notated import path
        to a statement comparison function.
        Defaults to ``LevenshteinDistance``.

    :param search_page_size:
        The maximum number of records to load into memory at a time when searching.
        Defaults to 1000
    """

    name = 'indexed_text_search'

    def __init__(self, chatbot, **kwargs):
        from lib.chatterbot.comparisons import LevenshteinDistance

        self.chatbot = chatbot

        statement_comparison_function = kwargs.get(
            'statement_comparison_function',
            LevenshteinDistance
        )

        self.compare_statements = statement_comparison_function(
            language=self.chatbot.storage.tagger.language
        )

        self.search_page_size = kwargs.get(
            'search_page_size', 1000
        )

    def search(self, input_statement, **additional_parameters):
        """
        Search for close matches to the input. Confidence scores for
        subsequent results will order of increasing value.

        :param input_statement: A statement.
        :type input_statement: chatterbot.conversation.Statement

        :param **additional_parameters: Additional parameters to be passed
            to the ``filter`` method of the storage adapter when searching.

        :rtype: Generator yielding one closest matching statement at a time.
        """
        self.chatbot.logger.info('Beginning search for close text match')

        input_search_in_response_to = input_statement.search_in_response_to

        if not input_statement.search_in_response_to:
            self.chatbot.logger.warn(
                'No value for search_in_response_to was available on the provided input'
            )

            input_search_in_response_to = self.chatbot.storage.tagger.get_bigram_pair_string(
                input_statement.in_response_to
            )

        search_parameters = {
            'search_in_response_to_contains': input_search_in_response_to,
            'persona_not_startswith': 'bot:',
            'page_size': self.search_page_size
        }

        if additional_parameters:
            search_parameters.update(additional_parameters)

        statement_list = self.chatbot.storage.filter(**search_parameters)

        closest_match = Statement(text='')
        closest_match.confidence = 0

        self.chatbot.logger.info('Processing search results')

        # Find the closest matching known statement
        for statement in statement_list:
            confidence = self.compare_statements(input_statement, statement)

            if confidence > closest_match.confidence:
                statement.confidence = confidence
                closest_match = statement

                self.chatbot.logger.info('Similar text found: {} {}'.format(
                    closest_match.in_response_to, confidence
                ))

                yield closest_match
