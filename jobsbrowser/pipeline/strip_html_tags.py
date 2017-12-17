import re

from . import app


@app.task
def strip_html_tags(offer):
    """
    HTML tags are redundant, get rid of them.
    """
    tag_regexp = re.compile('<.*?>')
    offer['description'] = re.sub(tag_regexp, ' ', offer['description'])
    return offer
