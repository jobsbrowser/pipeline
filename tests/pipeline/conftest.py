import os

import nltk
import pytest


def pytest_addoption(parser):
    parser.addoption(
        '--nltk-data',
        action='store',
        type='string',
        default='~/nltk_data',
    )
    parser.addoption(
        '--polish-stopwords',
        action='store',
        type='string',
        default=os.path.join(os.path.dirname(__file__), 'data', 'polish'),
    )


@pytest.fixture(scope='session', autouse=True)
def download_nltk_data_when_missing(pytestconfig):
    nltk_data_dir = os.path.expanduser(pytestconfig.option.nltk_data)
    nltk.data.path = [nltk_data_dir]
    if os.access(nltk_data_dir, os.R_OK):
        return
    os.makedirs(nltk_data_dir)
    nltk.download('stopwords', nltk_data_dir)


@pytest.fixture(scope='session', autouse=True)
def ensure_polish_stopwords_stored_in_nltk_data(pytestconfig):
    nltk_pl_stopwords = os.path.join(
        nltk.data.path[0],
        'corpora',
        'stopwords',
        'polish',
    )
    if os.access(nltk_pl_stopwords, os.R_OK):
        return
    user_pl_stopwords = os.path.expanduser(
        pytestconfig.option.polish_stopwords
    )
    with open(user_pl_stopwords, encoding='utf8') as f:
        stopwords = f.read()
    with open(nltk_pl_stopwords, 'w', encoding='utf8') as f:
        f.write(stopwords)
