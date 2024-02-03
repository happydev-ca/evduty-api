import aiohttp
from aioresponses import aioresponses
from unittest import IsolatedAsyncioTestCase
from evdutyapi import EVDutyApi
from evdutyapi import Station
from tests.api_response.station_response import StationResponse
from tests.api_response.terminal_response import TerminalResponse


class EVdutyApiTest(IsolatedAsyncioTestCase):

    async def test_async_get_stations(self):
        username = 'username'
        password = 'password'
        token = "token"
        json = [
            StationResponse().to_json(),
            StationResponse(terminals=[TerminalResponse().to_json(), TerminalResponse().to_json()]).to_json(),
        ]

        expected_stations = [Station.from_json(s) for s in json]

        with aioresponses() as evduty_server:
            evduty_server.post('https://api.evduty.net/v1/account/login',
                               status=200,
                               payload={'accessToken': token, 'expiresIn': 1000})

            evduty_server.get('https://api.evduty.net/v1/account/stations',
                              status=200,
                              payload=json)

            async with aiohttp.ClientSession() as session:
                api = EVDutyApi(username, password, session)

                stations = await api.async_get_stations()

                self.assertEqual(stations, expected_stations)

                evduty_server.assert_called_with('https://api.evduty.net/v1/account/login',
                                                 method="POST",
                                                 json={'device': {'id': '', 'model': '', 'type': 'ANDROID'}, 'email': username, 'password': password})
                evduty_server.assert_called_with('https://api.evduty.net/v1/account/stations',
                                                 method="GET")
