from datetime import timedelta, datetime
from http import HTTPStatus
from logging import Logger, getLogger
from typing import List

import aiohttp
from aiohttp import ClientResponseError, ClientResponse

from evdutyapi import Station, Terminal
from evdutyapi.api_response.charging_session_response import ChargingSessionResponse
from evdutyapi.api_response.station_response import StationResponse
from evdutyapi.api_response.terminal_details_response import TerminalDetailsResponse
from evdutyapi.charging_profile import Amp

LOGGER: Logger = getLogger(__package__)


class EVDutyApiError(ClientResponseError):
    pass


class EVDutyApiInvalidCredentialsError(EVDutyApiError):
    pass


class EVDutyApi:
    base_url = 'https://api.evduty.net'

    def __init__(self, username: str, password: str, session: aiohttp.ClientSession):
        self.username = username
        self.password = password
        self.session = session
        self.headers = {'Content-Type': 'application/json'}
        self.expires_at = datetime.now() - timedelta(seconds=1)

    async def async_authenticate(self) -> None:
        if datetime.now() < self.expires_at:
            return

        json = {'device': {'id': '', 'model': '', 'type': 'ANDROID'}, 'email': self.username, 'password': self.password}
        async with self.session.post(f'{self.base_url}/v1/account/login', json=json, headers=self.headers) as response:
            await self._log("async_authenticate", response)
            self._raise_on_authenticate_error(response)
            body = await response.json()
            self.headers['Authorization'] = 'Bearer ' + body['accessToken']
            self.expires_at = datetime.now() + timedelta(seconds=body['expiresIn'])

    @staticmethod
    def _raise_on_authenticate_error(response: ClientResponse):
        if response.status == HTTPStatus.BAD_REQUEST:
            raise EVDutyApiInvalidCredentialsError(response.request_info, response.history, status=response.status, message=response.reason, headers=response.headers)
        if not response.ok:
            raise EVDutyApiError(response.request_info, response.history, status=response.status, message=response.reason, headers=response.headers)

    async def async_get_stations(self) -> List[Station]:
        await self.async_authenticate()
        async with self.session.get(f'{self.base_url}/v1/account/stations', headers=self.headers) as response:
            await self._log("async_get_stations", response)
            await self._raise_on_get_error(response)
            json_stations = await response.json()
            stations = [StationResponse.from_json(s) for s in json_stations]
            await self._async_get_terminals(stations)
            await self._async_get_sessions(stations)
            return stations

    async def _async_get_terminals(self, stations: List[Station]) -> None:
        for station in stations:
            for terminal in station.terminals:
                async with self.session.get(f'{self.base_url}/v1/account/stations/{station.id}/terminals/{terminal.id}', headers=self.headers) as response:
                    await self._log("_async_get_terminals", response)
                    await self._raise_on_get_error(response)
                    json_terminal_details = await response.json()
                    terminal.network_info = TerminalDetailsResponse.from_json_to_network_info(json_terminal_details)
                    terminal.charging_profile = TerminalDetailsResponse.from_json_to_charging_profile(json_terminal_details)

    async def _async_get_sessions(self, stations: List[Station]) -> None:
        for station in stations:
            for terminal in station.terminals:
                async with self.session.get(f'{self.base_url}/v1/account/stations/{station.id}/terminals/{terminal.id}/session', headers=self.headers) as response:
                    await self._log("_async_get_sessions", response)
                    await self._raise_on_get_error(response)
                    if await response.text() != '':
                        json_session = await response.json()
                        terminal.session = ChargingSessionResponse.from_json(json_session)

    async def async_set_terminal_max_charging_current(self, terminal: Terminal, current: Amp) -> None:
        await self.async_authenticate()
        async with self.session.get(f'{self.base_url}/v1/account/stations/{terminal.station_id}/terminals/{terminal.id}', headers=self.headers) as response:
            await self._log("async_set_terminal_max_charging_current GET", response)
            await self._raise_on_get_error(response)
            json_request = await response.json()
            TerminalDetailsResponse.to_max_charging_current_request(json_request, current)
            async with self.session.put(f'{self.base_url}/v1/account/stations/{terminal.station_id}/terminals/{terminal.id}', headers=self.headers, json=json_request) as put_response:
                await self._log("async_set_terminal_max_charging_current PUT", response)
                await self._raise_on_get_error(put_response)

    async def _raise_on_get_error(self, response: ClientResponse):
        if response.status == HTTPStatus.UNAUTHORIZED:
            self.expires_at = datetime.now() - timedelta(seconds=1)
            del self.headers['Authorization']

        if not response.ok:
            raise EVDutyApiError(response.request_info, response.history, status=response.status, message=response.reason, headers=response.headers)

    @staticmethod
    async def _log(endpoint, response):
        LOGGER.debug(f"{endpoint} : status[{response.status}] - headers [{dict(response.headers)}] - body[{await response.text()}]")
