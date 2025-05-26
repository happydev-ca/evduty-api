import unittest

from evdutyapi.terminals.terminal_response import TerminalResponse
from .terminal_response_builder import TerminalResponseBuilder


class TerminalResponseTest(unittest.TestCase):
    def test_parses_response_to_network_info(self):
        response = TerminalResponseBuilder.default().build()

        network_info = TerminalResponse.from_json_to_network_info(response)

        self.assertEqual(network_info.wifi_ssid, response['wifiSSID'])
        self.assertEqual(network_info.wifi_rssi, response['wifiRSSI'])
        self.assertEqual(network_info.mac_address, response['macAddress'])
        self.assertEqual(network_info.ip_address, response['localIPAddress'])

    def test_parses_response_to_charging_profile_enabled(self):
        response = (TerminalResponseBuilder
                    .default()
                    .with_charging_rate(10)
                    .with_amperage(30)
                    .build())

        charging_profile = TerminalResponse.from_json_to_charging_profile(response)

        self.assertEqual(charging_profile.power_limitation, True)
        self.assertEqual(charging_profile.current_limit, 10)
        self.assertEqual(charging_profile.current_max, 30)

    def test_parses_json_to_charging_profile_disabled(self):
        response = (TerminalResponseBuilder
                    .default()
                    .without_charging_profile()
                    .with_amperage(30)
                    .build())

        charging_profile = TerminalResponse.from_json_to_charging_profile(response)

        self.assertEqual(charging_profile.power_limitation, False)
        self.assertEqual(charging_profile.current_limit, 30)
        self.assertEqual(charging_profile.current_max, 30)
