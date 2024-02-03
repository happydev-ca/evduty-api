import unittest

from evdutyapi.api_response.charging_session_response import ChargingSessionResponse


class ChargingSessionResponseTest(unittest.TestCase):
    def test_parses_json(self):
        json = ChargingSessionResponse(is_active=True).to_json()

        session = ChargingSessionResponse.from_json(json)

        self.assertEqual(session.is_active, True)
