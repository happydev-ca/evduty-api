from typing import Any, Dict
from evdutyapi import NetworkInfo
from evdutyapi.charging_profile import ChargingProfile


class TerminalDetailsResponse:
    def __init__(self, wifi_ssid, wifi_rssi, mac_address, ip_address, power_limitation, current_limit, amperage):
        self.wifi_ssid = wifi_ssid
        self.wifi_rssi = wifi_rssi
        self.mac_address = mac_address
        self.ip_address = ip_address
        self.power_limitation = power_limitation
        self.current_limit = current_limit
        self.amperage = amperage

    @classmethod
    def from_json_to_network_info(cls, data: Dict[str, Any]) -> NetworkInfo:
        return NetworkInfo(wifi_ssid=data['wifiSSID'],
                           wifi_rssi=data['wifiRSSI'],
                           mac_address=data['macAddress'],
                           ip_address=data['localIPAddress'])

    @classmethod
    def from_json_to_charging_profile(cls, data: Dict[str, Any]) -> ChargingProfile:
        current_max = data['amperage']
        power_limitation = 'chargingProfile' in data
        current_limit = data['chargingProfile']['chargingRate'] if power_limitation else current_max
        return ChargingProfile(power_limitation=power_limitation, current_limit=current_limit, current_max=current_max)

    @classmethod
    def to_max_charging_current_request(cls, data: Dict[str, Any], current) -> Dict[str, Any]:
        data.pop('cost', None)
        data.pop('alternateCost', None)
        data.pop('sessionTimeLimits', None)
        if data.get('costLocal') is None:
            data.pop('costLocal', None)
        data['chargingProfile'] = {'chargingRate': current, 'chargingRateUnit': 'A'}
        return data

    def to_json(self):
        json = {
            "amperage": self.amperage,
            "wifiSSID": self.wifi_ssid,
            "wifiRSSI": self.wifi_rssi,
            "macAddress": self.mac_address,
            "localIPAddress": self.ip_address
        }
        if self.power_limitation:
            json['chargingProfile'] = {
                "chargingRate": self.current_limit
            }
        return json
