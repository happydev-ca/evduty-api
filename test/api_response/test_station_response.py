import unittest

from evdutyapi import ChargingStatus
from evdutyapi.api_response.station_response import StationResponse


class StationResponseTest(unittest.TestCase):
    def test_parses_json(self):
        json = StationResponse(id="1", name="A", status="available", terminals=[]).to_json()

        station = StationResponse.from_json(json)

        self.assertEqual(station.id, "1")
        self.assertEqual(station.name, "A")
        self.assertEqual(station.status, ChargingStatus.available)
        self.assertEqual(station.terminals, [])
