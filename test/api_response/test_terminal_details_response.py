import unittest

from evdutyapi.api_response.terminal_details_response import TerminalDetailsResponse


class TerminalDetailsResponseTest(unittest.TestCase):
    def test_parses_json_to_network_info(self):
        json = TerminalDetailsResponse(wifi_ssid='wifi', wifi_rssi=-72, mac_address='mac', ip_address='ip', power_limitation=False, current_limit=30, amperage=30).to_json()

        network_info = TerminalDetailsResponse.from_json_to_network_info(json)

        self.assertEqual(network_info.wifi_ssid, 'wifi')
        self.assertEqual(network_info.wifi_rssi, -72)
        self.assertEqual(network_info.mac_address, 'mac')
        self.assertEqual(network_info.ip_address, 'ip')

    def test_parses_json_to_charging_profile_enabled(self):
        json = TerminalDetailsResponse(wifi_ssid='wifi', wifi_rssi=-72, mac_address='mac', ip_address='ip', power_limitation=True, current_limit=20, amperage=30).to_json()

        charging_profile = TerminalDetailsResponse.from_json_to_charging_profile(json)

        self.assertEqual(charging_profile.power_limitation, True)
        self.assertEqual(charging_profile.current_limit, 20)
        self.assertEqual(charging_profile.current_max, 30)

    def test_parses_json_to_charging_profile_disabled(self):
        json = TerminalDetailsResponse(wifi_ssid='wifi', wifi_rssi=-72, mac_address='mac', ip_address='ip', power_limitation=False, current_limit=0, amperage=30).to_json()

        charging_profile = TerminalDetailsResponse.from_json_to_charging_profile(json)

        self.assertEqual(charging_profile.power_limitation, False)
        self.assertEqual(charging_profile.current_limit, 30)
        self.assertEqual(charging_profile.current_max, 30)

    def test_create_request_from_response_removing_unmodifiable_fields(self):
        json = TerminalDetailsResponse(wifi_ssid='wifi', wifi_rssi=-72, mac_address='mac', ip_address='ip', power_limitation=False, current_limit=0, amperage=30).to_json()
        json['cost'] = 'any'
        json['alternateCost'] = 'any'
        json['sessionTimeLimits'] = 'any'
        json['costLocal'] = None

        request = TerminalDetailsResponse.to_max_charging_current_request(json, 10)

        self.assertEqual('cost' in request, False)
        self.assertEqual('alternateCost' in request, False)
        self.assertEqual('sessionTimeLimits' in request, False)
        self.assertEqual('costLocal' in request, False)
        self.assertEqual(request['chargingProfile']['chargingRate'], 10)
        self.assertEqual(request['chargingProfile']['chargingRateUnit'], 'A')

    def test_create_request_from_response_keeping_cost_local_when_set(self):
        json = TerminalDetailsResponse(wifi_ssid='wifi', wifi_rssi=-72, mac_address='mac', ip_address='ip', power_limitation=False, current_limit=0, amperage=30).to_json()
        json['costLocal'] = 0.1034

        request = TerminalDetailsResponse.to_max_charging_current_request(json, 10)

        self.assertEqual(request['costLocal'], 0.1034)
