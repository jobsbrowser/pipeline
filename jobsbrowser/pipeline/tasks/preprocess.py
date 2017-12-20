import re

from nltk import corpus

from .. import app
from .utils import lower_word_tokenize
from .exceptions import LanguageNotSupported


@app.task
def prepare(offer):
    """
    For further processing we need nothing more than
    offer id, description and title.
    """
    simplified_offer = {
        'id': offer['offer_id'],
        'description': ' '.join([
            offer.get('job_qualifications', ''),
            offer.get('job_description', '')
        ]),
        'title': offer['job_title']
    }
    return simplified_offer


@app.task
def strip_html_tags(offer):
    """
    HTML tags are redundant, get rid of them.
    """
    tag_regexp = re.compile('<.*?>')
    offer['description'] = re.sub(tag_regexp, ' ', offer['description'])
    return offer


@app.task
def tokenize(offer):
    """
    Tokenize and lowercase offer description using nltk
    """
    offer['description'] = lower_word_tokenize(offer['description'])
    return offer


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
