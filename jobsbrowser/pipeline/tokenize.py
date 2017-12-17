from nltk import word_tokenize

from . import app


@app.task
def tokenize(offer):
    """
    Tokenize and lowercase offer description using nltk
    """
    offer['description'] = word_tokenize(offer['description'].lower())
    return offer
