from nltk import corpus

from . import app


class LanguageNotSupported(Exception):
    pass


@app.task
def detect_language(offer):
    """
    Accept only polish language
    """
    languages = {
        'english': {
            'stopwords': corpus.stopwords.words('english'),
            'counter': 0
        },
        'polish': {
            'stopwords': corpus.stopwords.words('polish'),
            'counter': 0
        }
    }
    for word in offer['description']:
        for language in languages.values():
            if word in language['stopwords']:
                language['counter'] += 1
    if max(languages, key=lambda l: languages[l]['counter']) == 'polish':
        return offer
    else:
        raise LanguageNotSupported
