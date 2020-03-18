import responses
from django.test import TestCase
from django.test.utils import override_settings

from weblate.checks.tests.test_checks import MockUnit
from weblate.machinery.google import GoogleTranslationAdvanced


class MachineTranslationTest(TestCase):
    """Testing of machine translation core."""

    def get_machine(self, cls, cache=False):
        machine = cls()
        machine.delete_cache()
        machine.cache_translations = cache
        return machine

    def assert_translate(self, machine, lang="cs", word="world", empty=False):
        translation = machine.translate(lang, word, MockUnit(), None)
        self.assertIsInstance(translation, list)
        if not empty:
            self.assertTrue(translation)
        for result in translation:
            for key, value in result.items():
                if key == "quality":
                    self.assertIsInstance(
                        value, int, "'{}' is supposed to be a integer".format(key)
                    )
                else:
                    self.assertIsInstance(
                        value, str, "'{}' is supposed to be a string".format(key)
                    )

    @override_settings(
        MT_GOOGLE_CREDENTIALS="/home/filip/credentials/Translating-c6687319a486.json",
        MT_GOOGLE_PROJECT="translating-271108",
    )
    @responses.activate
    def test_google_translate_advanced(self):
        machine = self.get_machine(GoogleTranslationAdvanced)
        responses.add(
            responses.POST,
            "https://oauth2.googleapis.com/token",
            json={
                "access_token": "Bearer lHrrFiBohImhRbgzQvsmSoEvIMtnEFmP",
                "token_type": "bearer",
            },
            status=200,
        )
        responses.add(
            responses.GET,
            "https://translation.googleapis.com/v3/"
            "Translating-c6687319a486/supportedLanguages",
            json={
                "languages": [
                    {
                        "languageCode": "en",
                        "displayName": "",
                        "supportSource": True,
                        "supportTarget": True,
                    },
                    {
                        "languageCode": "cs",
                        "displayName": "",
                        "supportSource": True,
                        "supportTarget": True,
                    },
                ]
            },
            status=200,
        )
        self.assert_translate(machine, "es", word="Test")
