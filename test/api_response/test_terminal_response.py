import unittest

from evdutyapi import ChargingStatus, ChargingSession
from evdutyapi.api_response.terminal_response import TerminalResponse


class TerminalResponseTest(unittest.TestCase):
    def test_parses_json(self):
        json = TerminalResponse(id="1", name="A", status="inUse", charge_box_identity="model", firmware_version="1.1.1").to_json()

        terminal = TerminalResponse.from_json(json, "2")

        self.assertEqual(terminal.id, "1")
        self.assertEqual(terminal.station_id, "2")
        self.assertEqual(terminal.name, "A")
        self.assertEqual(terminal.status, ChargingStatus.in_use)
        self.assertEqual(terminal.charge_box_identity, "model")
        self.assertEqual(terminal.firmware_version, "1.1.1")
        self.assertEqual(terminal.session, ChargingSession.no_session())
