import unittest

from evdutyapi.api_response.terminal_details_response import TerminalDetailsResponse


class TerminalDetailsResponseTest(unittest.TestCase):
    def test_parses_json(self):
        json = TerminalDetailsResponse(wifi_ssid='wifi', wifi_rssi=-72, mac_address='mac', ip_address='ip').to_json()

        network_info = TerminalDetailsResponse.from_json(json)

        self.assertEqual(network_info.wifi_ssid, 'wifi')
        self.assertEqual(network_info.wifi_rssi, -72)
        self.assertEqual(network_info.mac_address, 'mac')
        self.assertEqual(network_info.ip_address, 'ip')
