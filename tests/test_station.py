import unittest

from evdutyapi import Station, StationStatus
from tests.api_response.station_response import StationResponse


class StationTest(unittest.TestCase):
    def test_parses_json(self):
        json = StationResponse(id="1", name="A", status="available").to_json()

        station = Station.from_json(json)

        self.assertEqual(station.id, "1")
        self.assertEqual(station.name, "A")
        self.assertEqual(station.status, StationStatus.available)
        self.assertEqual(station.terminals, [])
