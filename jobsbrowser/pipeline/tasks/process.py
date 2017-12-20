from .. import app
from .bases import TagsFindingTask


@app.task(base=TagsFindingTask)
def find_tags(offer):
    """Find stacoverflow tags in offer.
    """
    return find_tags.find_tags(offer)
