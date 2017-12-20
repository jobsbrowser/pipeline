import pytest

from jobsbrowser.pipeline.remove_stopwords import remove_stopwords


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
