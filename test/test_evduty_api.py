import aiohttp
from aioresponses import aioresponses
from unittest import IsolatedAsyncioTestCase
from evdutyapi import EVDutyApi
from evdutyapi.api_response.charging_session_response import ChargingSessionResponse
from evdutyapi.api_response.station_response import StationResponse
from evdutyapi.api_response.terminal_response import TerminalResponse


class EVdutyApiTest(IsolatedAsyncioTestCase):

    async def test_async_get_stations(self):
        username = 'username'
        password = 'password'
        token = "token"
        get_stations_response = [
            StationResponse(id="station_id", name="station_name", status="available", terminals=[
                TerminalResponse(id="terminal_id", name="terminal_name", status="inUse", charge_box_identity="identity", firmware_version="version").to_json()
            ]).to_json(),
        ]
        get_session_response = (ChargingSessionResponse(is_active=True,
                                                        is_charging=True,
                                                        volt=240,
                                                        amp=13.9,
                                                        power=3336,
                                                        energy_consumed=36459.92,
                                                        charge_start_date=1706897191,
                                                        duration=77602.7,
                                                        cost_local=0.10039)
                                .to_json())

        expected_stations = [StationResponse.from_json(s) for s in get_stations_response]

        with aioresponses() as evduty_server:
            evduty_server.post('https://api.evduty.net/v1/account/login',
                               status=200,
                               payload={'accessToken': token, 'expiresIn': 1000})

            evduty_server.get('https://api.evduty.net/v1/account/stations',
                              status=200,
                              payload=get_stations_response)

            evduty_server.get('https://api.evduty.net/v1/account/stations/station_id/terminals/terminal_id/session',
                              status=200,
                              payload=get_session_response)

            async with aiohttp.ClientSession() as session:
                api = EVDutyApi(username, password, session)

                stations = await api.async_get_stations()

                self.assertEqual(stations, expected_stations)

                evduty_server.assert_called_with('https://api.evduty.net/v1/account/login',
                                                 method="POST",
                                                 json={'device': {'id': '', 'model': '', 'type': 'ANDROID'}, 'email': username, 'password': password})
