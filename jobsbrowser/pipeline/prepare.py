from . import app


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
