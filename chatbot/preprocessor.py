import re
import string


def clean_url(text):
    """
    Remove any https from the statement text.
    """

    text = re.sub(r"(http://\S+|https://\S+)", "", text)

    return text


def convert_emojis(text):
    """Convert emoji to text

    Args:
        text (str): text to preprocess

    Returns:
        str
    """
    # Some emoji regex token
    emoji2text = {
        r"(:|=)\s*\)+": "cười",
        r"(:|=)\s*\(+": "buồn",
        r"\^\s*(_|-)?\s*\^": "dễ thương",
        r"T\s*(_|-)?\s*T": "khóc",
        r"(:|=)\s*(v|V)+": "láo",
        r"\?+": "hỏi",
        r"!+": "cảm",
    }

    for emo, word in emoji2text.items():
        text = re.sub(emo, ' ' + word, text)
    return text

def clean_whitespace(text):
    """Remove trailing whitespace
    """
    return re.sub(r'\s{2,}', ' ', text)

def remove_punct(text):
    """Remove punctuation from text

    Args:
        text (str): text to preprocess
    """

    return text.translate(str.maketrans('', '', string.punctuation + string.digits))

