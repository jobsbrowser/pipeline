import pytest

from jobsbrowser.pipeline.strip_html_tags import strip_html_tags


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
