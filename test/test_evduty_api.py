import asyncio

import aiohttp
from unittest import IsolatedAsyncioTestCase
from evdutyapi import EVDutyApi
from evdutyapi.api_response.charging_session_response import ChargingSessionResponse
from evdutyapi.api_response.station_response import StationResponse
from evdutyapi.api_response.terminal_response import TerminalResponse
from test.test_support.evduty_server_for_test import EVDutyServerForTest


class EVdutyApiTest(IsolatedAsyncioTestCase):
    base_url = 'https://api.evduty.net'
    username = 'username'
    password = 'password'

    async def test_authenticate_user(self):
        with EVDutyServerForTest() as evduty_server:
            await evduty_server.prepare_login_response({'accessToken': 'hello', 'expiresIn': 43200})

            async with aiohttp.ClientSession() as session:
                api = EVDutyApi(self.username, self.password, session)
                await api.async_authenticate()

                evduty_server.assert_called_with(url='/v1/account/login',
                                                 method='POST',
                                                 headers={'Content-Type': 'application/json'},
                                                 json={'device': {'id': '', 'model': '', 'type': 'ANDROID'}, 'email': self.username, 'password': self.password})

    async def test_reuse_token_when_it_is_valid(self):
        with EVDutyServerForTest() as evduty_server:
            await evduty_server.prepare_login_response({'accessToken': 'hello', 'expiresIn': 1000})

            async with aiohttp.ClientSession() as session:
                api = EVDutyApi(self.username, self.password, session)
                await api.async_authenticate()
                await api.async_authenticate()

                evduty_server.assert_called_n_times_with(times=1,
                                                         url='/v1/account/login',
                                                         method='POST',
                                                         headers={'Content-Type': 'application/json'},
                                                         json={'device': {'id': '', 'model': '', 'type': 'ANDROID'}, 'email': self.username, 'password': self.password})

    async def test_reauthorize_when_token_is_invalid(self):
        with EVDutyServerForTest() as evduty_server:
            await evduty_server.prepare_login_response({'accessToken': 'hello', 'expiresIn': 0})

            async with aiohttp.ClientSession() as session:
                api = EVDutyApi(self.username, self.password, session)
                await api.async_authenticate()
                await asyncio.sleep(0)
                await api.async_authenticate()

                evduty_server.assert_called_n_times_with(times=2,
                                                         url='/v1/account/login',
                                                         method='POST',
                                                         headers={'Content-Type': 'application/json', 'Authorization': 'Bearer hello'},
                                                         json={'device': {'id': '', 'model': '', 'type': 'ANDROID'}, 'email': self.username, 'password': self.password})

    async def test_async_get_stations(self):
        with EVDutyServerForTest() as evduty_server:
            stations_response = await self.any_stations_response()
            session_response = await self.any_session_response()

            await evduty_server.prepare_login_response()
            await evduty_server.prepare_stations_response(stations_response)
            await evduty_server.prepare_session_response(session_response)

            async with aiohttp.ClientSession() as session:
                api = EVDutyApi(self.username, self.password, session)
                stations = await api.async_get_stations()

                expected_stations = [StationResponse.from_json(s) for s in stations_response]
                self.assertEqual(stations, expected_stations)

    @staticmethod
    async def any_stations_response():
        return [
            StationResponse(id='station_id', name='station_name', status='available', terminals=[
                TerminalResponse(id='terminal_id', name='terminal_name', status='inUse', charge_box_identity='identity', firmware_version='version').to_json()
            ]).to_json(),
        ]

    @staticmethod
    async def any_session_response():
        return (ChargingSessionResponse(is_active=True, is_charging=True, volt=240, amp=13.9, power=3336,
                                        energy_consumed=36459.92, charge_start_date=1706897191, duration=77602.7, cost_local=0.10039).to_json())
