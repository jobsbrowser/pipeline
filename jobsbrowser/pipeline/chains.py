from celery import chain

from .tasks import (
    detect_language,
    find_tags,
    prepare,
    remove_stopwords,
    save_to_mongodb,
    strip_html_tags,
    tokenize,
)

pracuj_pipeline = chain(
    prepare.s(),
    strip_html_tags.s(),
    tokenize.s(),
    detect_language.s(),
    remove_stopwords.s(),
    find_tags.s(),
    save_to_mongodb.s(),
)
