from unittest import IsolatedAsyncioTestCase
from aioresponses import aioresponses
from evdutyapi import EVDutyApi


class EVdutyApiTest(IsolatedAsyncioTestCase):

    async def test_async_get_stations(self):
        username = 'username'
        password = 'password'
        token = "token"
        expected_stations = [{"station1": "value1"}, {"station2": "value2"}]

        with aioresponses() as evduty_server:
            evduty_server.post('https://api.evduty.net/v1/account/login',
                               status=200,
                               payload={'accessToken': token, 'expiresIn': 1000})

            evduty_server.get('https://api.evduty.net/v1/account/stations',
                              status=200,
                              payload=expected_stations)

            async with EVDutyApi(username, password) as api:
                stations = await api.async_get_stations()
                self.assertEqual(stations, expected_stations)

                evduty_server.assert_called_with('https://api.evduty.net/v1/account/login',
                                                 method="POST",
                                                 json={'device': {'id': '', 'model': '', 'type': 'ANDROID'}, 'email': username, 'password': password})
                evduty_server.assert_called_with('https://api.evduty.net/v1/account/stations',
                                                 method="GET")
