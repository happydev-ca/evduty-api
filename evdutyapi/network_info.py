from dataclasses import dataclass


@dataclass(frozen=True)
class NetworkInfo:
    wifi_ssid: str
    wifi_rssi: int
    mac_address: str
    ip_address: str
