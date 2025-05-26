import asyncio
from http import HTTPStatus

import aiohttp
from unittest import IsolatedAsyncioTestCase

from evdutyapi import (ChargingStatus, EVDutyApi, ChargingSession, Terminal,
                       EVDutyApiError, EVDutyApiInvalidCredentialsError)
from evdutyapi.charging_sessions.charging_session_response import ChargingSessionResponse
from evdutyapi.max_charging_current.max_charging_current_request import MaxChargingCurrentRequest
from evdutyapi.stations.station_response import StationResponse
from evdutyapi.terminals.terminal_response import TerminalResponse
from .evduty_server_for_test import EVDutyServerForTest
from .stations.station_response_builder import StationResponseBuilder
from .terminals.terminal_response_builder import TerminalResponseBuilder
from .charging_sessions.charging_session_response_builder import ChargingSessionResponseBuilder


class EVdutyApiTest(IsolatedAsyncioTestCase):
    base_url = 'https://api.evduty.net'
    username = 'username'
    password = 'password'

    async def test_authenticate_user(self):
        with EVDutyServerForTest() as evduty_server:
            evduty_server.prepare_login_response({'accessToken': 'hello', 'expiresIn': 43200})

            async with aiohttp.ClientSession() as session:
                api = EVDutyApi(self.username, self.password, session)
                await api.async_authenticate()

                evduty_server.assert_called_with(url='/v1/account/login',
                                                 method='POST',
                                                 headers={'Content-Type': 'application/json'},
                                                 json={'device': {'id': '', 'model': '', 'type': 'ANDROID'},
                                                       'email': self.username, 'password': self.password})

    async def test_authenticate_invalid_credentials_error(self):
        with EVDutyServerForTest() as evduty_server:
            evduty_server.prepare_login_response(status=HTTPStatus.BAD_REQUEST)

            async with aiohttp.ClientSession() as session:
                api = EVDutyApi(self.username, self.password, session)

                with self.assertRaises(EVDutyApiInvalidCredentialsError):
                    await api.async_authenticate()

    async def test_authenticate_other_error(self):
        with EVDutyServerForTest() as evduty_server:
            evduty_server.prepare_login_response(status=HTTPStatus.SERVICE_UNAVAILABLE)

            async with aiohttp.ClientSession() as session:
                api = EVDutyApi(self.username, self.password, session)

                with self.assertRaises(EVDutyApiError):
                    await api.async_authenticate()

    async def test_reuse_token_when_it_is_valid(self):
        with EVDutyServerForTest() as evduty_server:
            evduty_server.prepare_login_response({'accessToken': 'hello', 'expiresIn': 1000})

            async with aiohttp.ClientSession() as session:
                api = EVDutyApi(self.username, self.password, session)
                await api.async_authenticate()
                await api.async_authenticate()

                evduty_server.assert_called_n_times_with(times=1,
                                                         url='/v1/account/login',
                                                         method='POST',
                                                         headers={'Content-Type': 'application/json'},
                                                         json={'device': {'id': '', 'model': '', 'type': 'ANDROID'},
                                                               'email': self.username, 'password': self.password})

    async def test_reauthorize_when_token_expires(self):
        with EVDutyServerForTest() as evduty_server:
            evduty_server.prepare_login_response({'accessToken': 'hello', 'expiresIn': 0})

            async with aiohttp.ClientSession() as session:
                api = EVDutyApi(self.username, self.password, session)
                await api.async_authenticate()
                await asyncio.sleep(0)
                await api.async_authenticate()

                evduty_server.assert_called_n_times_with(times=2,
                                                         url='/v1/account/login',
                                                         method='POST',
                                                         headers={'Content-Type': 'application/json',
                                                                  'Authorization': 'Bearer hello'},
                                                         json={'device': {'id': '', 'model': '', 'type': 'ANDROID'},
                                                               'email': self.username, 'password': self.password})

    async def test_reauthorize_when_token_is_invalid(self):
        with EVDutyServerForTest() as evduty_server:
            evduty_server.prepare_login_response({'accessToken': 'hello', 'expiresIn': 1000})
            evduty_server.prepare_stations_response(status=HTTPStatus.UNAUTHORIZED, repeat=False)

            async with aiohttp.ClientSession() as session:
                api = EVDutyApi(self.username, self.password, session)
                try:
                    await api.async_get_stations()
                except EVDutyApiError:
                    pass

                await api.async_authenticate()

                evduty_server.assert_called_n_times_with(times=2,
                                                         url='/v1/account/login',
                                                         method='POST',
                                                         headers={'Content-Type': 'application/json'},
                                                         json={'device': {'id': '', 'model': '', 'type': 'ANDROID'},
                                                               'email': self.username, 'password': self.password})

    async def test_async_get_stations(self):
        with EVDutyServerForTest() as evduty_server:
            stations_response = [StationResponseBuilder.default().build()]
            terminal_response = TerminalResponseBuilder.default().build()
            session_response = ChargingSessionResponseBuilder.default().build()

            evduty_server.prepare_login_response()
            evduty_server.prepare_stations_response(stations_response)
            evduty_server.prepare_terminal_details_response(terminal_response)
            evduty_server.prepare_session_response(session_response)

            async with aiohttp.ClientSession() as session:
                api = EVDutyApi(self.username, self.password, session)
                stations = await api.async_get_stations()

                expected_stations = [StationResponse.from_json(s) for s in stations_response]
                expected_stations[0].terminals[0].network_info = TerminalResponse.from_json_to_network_info(terminal_response)
                expected_stations[0].terminals[0].charging_profile = TerminalResponse.from_json_to_charging_profile(terminal_response)
                expected_stations[0].terminals[0].session = ChargingSessionResponse.from_json(session_response)
                self.assertEqual(stations, expected_stations)

    async def test_async_no_charging_session(self):
        with EVDutyServerForTest() as evduty_server:
            evduty_server.prepare_login_response()
            evduty_server.prepare_stations_response([StationResponseBuilder.default().build()])
            evduty_server.prepare_terminal_details_response(TerminalResponseBuilder.default().build())
            evduty_server.prepare_session_response(None)

            async with aiohttp.ClientSession() as session:
                api = EVDutyApi(self.username, self.password, session)
                stations = await api.async_get_stations()

                self.assertEqual(stations[0].terminals[0].session, ChargingSession.no_session())

    async def test_async_set_terminal_max_charging_current(self):
        with EVDutyServerForTest() as evduty_server:
            evduty_server.prepare_login_response()
            terminal_response = TerminalResponseBuilder.default().build()
            evduty_server.prepare_terminal_details_response(terminal_response)
            evduty_server.prepare_put_terminal_details()

            async with aiohttp.ClientSession() as session:
                api = EVDutyApi(self.username, self.password, session)
                terminal = Terminal(id='terminal_id',
                                    station_id='station_id',
                                    name='',
                                    status=ChargingStatus.available,
                                    charge_box_identity='',
                                    firmware_version='',
                                    session=ChargingSession.no_session())
                await api.async_set_terminal_max_charging_current(terminal, current=15)

                evduty_server.assert_called_with(
                    url='/v1/account/stations/station_id/terminals/terminal_id',
                    method='PUT',
                    data=None,
                    headers={'Content-Type': 'application/json', 'Authorization': 'Bearer token'},
                    json=MaxChargingCurrentRequest.from_terminal_response(terminal_response, 15))
