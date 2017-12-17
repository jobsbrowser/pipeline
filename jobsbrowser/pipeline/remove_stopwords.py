from nltk import corpus

from . import app


@app.task
def remove_stopwords(offer):
    """
    Remove stopwords from offer description
    """
    stopwords = corpus.stopwords.words('polish')
    offer['description'] = [
        token for token in offer['description']
        if token not in stopwords
    ]
    return offer
