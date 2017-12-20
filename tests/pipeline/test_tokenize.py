import pytest

from jobsbrowser.pipeline.tokenize import tokenize


@pytest.mark.parametrize('offer_description, expected_description', [
    ('SPAM', ['spam']),
    ('no tags at all', 'no tags at all'.split()),
    ('SPAM. Foo-bar', ['spam', '.', 'foo-bar']),
])
def test_strip_html_tags_return_tokens_whithout_html_tags(
    offer_description,
    expected_description,
):
    description = tokenize({'description': offer_description}).get(
        'description',
    )
    assert description == expected_description
