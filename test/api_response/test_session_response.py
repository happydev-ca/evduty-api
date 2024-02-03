import unittest

from evdutyapi.api_response.session_response import SessionResponse


class SessionResponseTest(unittest.TestCase):
    def test_parses_json(self):
        json = SessionResponse(is_active=True).to_json()

        session = SessionResponse.from_json(json)

        self.assertEqual(session.is_active, True)
