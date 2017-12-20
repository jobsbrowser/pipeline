import pytest

from jobsbrowser.pipeline.detect_language import (
    detect_language,
    LanguageNotSupported,
)


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
