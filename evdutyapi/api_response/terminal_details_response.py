from typing import Any, Dict
from evdutyapi import NetworkInfo


class TerminalDetailsResponse:
    def __init__(self, wifi_ssid, wifi_rssi, mac_address, ip_address):
        self.wifi_ssid = wifi_ssid
        self.wifi_rssi = wifi_rssi
        self.mac_address = mac_address
        self.ip_address = ip_address

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> NetworkInfo:
        return NetworkInfo(wifi_ssid=data['wifiSSID'],
                           wifi_rssi=data['wifiRSSI'],
                           mac_address=data['macAddress'],
                           ip_address=data['localIPAddress'])

    def to_json(self):
        return {
            "wifiSSID": self.wifi_ssid,
            "wifiRSSI": self.wifi_rssi,
            "macAddress": self.mac_address,
            "localIPAddress": self.ip_address
        }
