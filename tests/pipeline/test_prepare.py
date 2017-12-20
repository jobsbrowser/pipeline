import pytest

from jobsbrowser.pipeline.prepare import prepare


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
