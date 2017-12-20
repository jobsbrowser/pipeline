from nltk import word_tokenize

from . import app


def lower_word_tokenize(text):
    return word_tokenize(text.lower())


@app.task
def tokenize(offer):
    """
    Tokenize and lowercase offer description using nltk
    """
    offer['description'] = lower_word_tokenize(offer['description'])
    return offer
