import unittest

from evdutyapi import Terminal, TerminalStatus
from tests.api_response.terminal_response import TerminalResponse


class TerminalTest(unittest.TestCase):
    def test_parses_json(self):
        json = TerminalResponse(id="1", name="A", status="inUse", charge_box_identity="model", firmware_version="1.1.1").to_json()

        station = Terminal.from_json(json)

        self.assertEqual(station.id, "1")
        self.assertEqual(station.name, "A")
        self.assertEqual(station.status, TerminalStatus.in_use)
        self.assertEqual(station.charge_box_identity, "model")
        self.assertEqual(station.firmware_version, "1.1.1")
