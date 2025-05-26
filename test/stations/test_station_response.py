import unittest

from evdutyapi import ChargingSession, ChargingStatus
from evdutyapi.stations.station_response import StationResponse
from .station_response_builder import StationResponseBuilder


class StationResponseTest(unittest.TestCase):
    def test_parses_response(self):
        response = StationResponseBuilder.default().build()

        station = StationResponse.from_json(response)

        self.assertEqual(station.id, response['id'])
        self.assertEqual(station.name, response['name'])
        terminals = [StationResponse.terminal_from_json(terminal, station.id) for terminal in response['terminals']]
        self.assertEqual(station.terminals, terminals)

    def test_parses_terminal_response(self):
        response = StationResponseBuilder.default().build()['terminals'][0]

        terminal = StationResponse.terminal_from_json(response, 'station_id')

        self.assertEqual(terminal.id, response['id'])
        self.assertEqual(terminal.station_id, 'station_id')
        self.assertEqual(terminal.name, response['name'])
        self.assertEqual(terminal.status, ChargingStatus(response['status']))
        self.assertEqual(terminal.charge_box_identity, response['chargeBoxIdentity'])
        self.assertEqual(terminal.firmware_version, response['firmwareVersion'])
        self.assertEqual(terminal.session, ChargingSession.no_session())
