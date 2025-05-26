import unittest
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from evdutyapi.charging_sessions.charging_session_response import ChargingSessionResponse
from .charging_session_response_builder import ChargingSessionResponseBuilder


class ChargingSessionResponseTest(unittest.TestCase):
    def test_parses_response(self):
        response = ChargingSessionResponseBuilder.default().build()

        session = ChargingSessionResponse.from_json(response)

        self.assertEqual(session.is_active, response['isActive'])
        self.assertEqual(session.is_charging, response['isCharging'])
        self.assertEqual(session.volt, response['volt'])
        self.assertEqual(session.amp, response['amp'])
        self.assertEqual(session.power, response['power'])
        self.assertEqual(session.energy_consumed, response['energyConsumed'])
        self.assertEqual(session.start_date, datetime.fromtimestamp(response['chargeStartDate'], ZoneInfo('US/Eastern')))
        self.assertEqual(session.duration, timedelta(seconds=response['duration']))
        self.assertEqual(session.cost, round(response['station']['terminal']['costLocal'] * (response['energyConsumed'] / 1000), 2))

    def test_parses_response_without_cost_local(self):
        response = ChargingSessionResponseBuilder.default().with_cost(None).build()

        session = ChargingSessionResponse.from_json(response)

        self.assertEqual(session.cost, 0)
