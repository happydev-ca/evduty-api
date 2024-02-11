class NetworkInfo:
    def __init__(self, wifi_ssid: str, wifi_rssi: int, mac_address: str, ip_address: str):
        self.wifi_ssid = wifi_ssid
        self.wifi_rssi = wifi_rssi
        self.mac_address = mac_address
        self.ip_address = ip_address

    def __repr__(self) -> str:
        return f"<NetworkInfo wifi_ssid:{self.wifi_ssid} wifi_rssi:{self.wifi_rssi} mac_address:{self.mac_address} ip_address:{self.ip_address}>"

    def __eq__(self, __value):
        return (self.wifi_ssid == __value.wifi_ssid and
                self.wifi_rssi == __value.wifi_rssi and
                self.mac_address == __value.mac_address and
                self.ip_address == __value.ip_address)
