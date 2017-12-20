import pytest

from jobsbrowser.pipeline.tasks import (
    detect_language,
    prepare,
    remove_stopwords,
    strip_html_tags,
    tokenize,
)
from jobsbrowser.pipeline.tasks.exceptions import LanguageNotSupported


class TestDetectLanguageTask:
    @pytest.mark.parametrize('offer', [
        {'description': 'to jest polski, więc nie może być błędów.'.split()},
        {'description': 'ależ tekst po polsku, to taki piękny język.'.split()},
    ])
    def test_detect_language_properly_detect_polish_language(self, offer):
        assert detect_language(offer) == offer

    @pytest.mark.parametrize('offer', [
        {'description': 'this is english description, no raise error'.split()},
        {'description': 'das ist ein satz auf deutsch'.split()},
    ])
    def test_detect_language_raise_error_for_not_supported_language(
        self,
        offer,
    ):
        with pytest.raises(LanguageNotSupported):
            detect_language(offer)


@pytest.mark.parametrize('offer, expected', [
    (
        {
            'offer_id': '1',
            'job_description': 'Ala ma kota!',
            'job_title': 'Title',
        },
        {'id': '1', 'description': ' Ala ma kota!', 'title': 'Title'},
    ),
    (
        {
            'offer_id': '1',
            'job_description': 'more spam!',
            'job_qualifications': 'spam!',
            'job_title': 'Title',
            'foobar': 'NiNiNi!',
        },
        {'id': '1', 'description': 'spam! more spam!', 'title': 'Title'},
    ),
])
def test_prepare_extract_proper_fields_from_offer(offer, expected):
    assert prepare(offer) == expected


@pytest.mark.parametrize('offer_description, expected_description', [
    ('to jest język polski'.split(), 'to język polski'.split()),
    ('ależ bogaty tekst po polsku.'.split(), 'bogaty tekst polsku.'.split()),
])
def test_remove_stopwords_return_tokens_without_stopwords(
    offer_description,
    expected_description,
):
    description = remove_stopwords({'description': offer_description}).get(
        'description',
    )
    assert description == expected_description


@pytest.mark.parametrize('offer_description, expected_description', [
    ('<body>SPAM</body>', ' SPAM '),
    ('no tags at all', 'no tags at all'),
    ('<div class="container"><p>SPAM</p></div>', '  SPAM  '),
])
def test_strip_html_tags_return_tokens_whithout_html_tags(
    offer_description,
    expected_description,
):
    description = strip_html_tags({'description': offer_description}).get(
        'description',
    )
    assert description == expected_description


@pytest.mark.parametrize('offer_description, expected_description', [
    ('SPAM', ['spam']),
    ('no tags at all', 'no tags at all'.split()),
    ('SPAM. Foo-bar', ['spam', '.', 'foo-bar']),
])
def test_tokenize_return_list_of_lowercase_tokens(
    offer_description,
    expected_description,
):
    description = tokenize({'description': offer_description}).get(
        'description',
    )
    assert description == expected_description
