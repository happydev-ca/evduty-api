import unittest
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from evdutyapi.api_response.charging_session_response import ChargingSessionResponse


class ChargingSessionResponseTest(unittest.TestCase):
    def test_parses_json(self):
        json = (ChargingSessionResponse(is_active=True,
                                        is_charging=False,
                                        volt=240,
                                        amp=13.9,
                                        power=3336,
                                        energy_consumed=36459.92,
                                        charge_start_date=1706897191,
                                        duration=77602.7,
                                        cost_local=0.10039999999999999)
                .to_json())

        session = ChargingSessionResponse.from_json(json)

        self.assertEqual(session.is_active, True)
        self.assertEqual(session.is_charging, False)
        self.assertEqual(session.volt, 240)
        self.assertEqual(session.amp, 13.9)
        self.assertEqual(session.power, 3336)
        self.assertEqual(session.energy_consumed, 36459.92)
        self.assertEqual(session.start_date, datetime(2024, 2, 2, 13, 6, 31, tzinfo=ZoneInfo('US/Eastern')))
        self.assertEqual(session.duration, timedelta(seconds=77602.7))
        self.assertEqual(session.cost, 3.66)
