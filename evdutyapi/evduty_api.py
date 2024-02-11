from datetime import timedelta, datetime
from http import HTTPStatus
from typing import List

import aiohttp
from aiohttp import ClientResponseError, ClientResponse

from evdutyapi import Station
from evdutyapi.api_response.charging_session_response import ChargingSessionResponse
from evdutyapi.api_response.station_response import StationResponse
from evdutyapi.api_response.terminal_details_response import TerminalDetailsResponse


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
                    await self._raise_on_get_error(response)
                    json_terminal_details = await response.json()
                    terminal.network_info = TerminalDetailsResponse.from_json(json_terminal_details)

    async def _async_get_sessions(self, stations: List[Station]) -> None:
        for station in stations:
            for terminal in station.terminals:
                async with self.session.get(f'{self.base_url}/v1/account/stations/{station.id}/terminals/{terminal.id}/session', headers=self.headers) as response:
                    await self._raise_on_get_error(response)
                    if await response.text() != '':
                        json_session = await response.json()
                        terminal.session = ChargingSessionResponse.from_json(json_session)

    async def _raise_on_get_error(self, response: ClientResponse):
        if response.status == HTTPStatus.UNAUTHORIZED:
            self.expires_at = datetime.now() - timedelta(seconds=1)
            del self.headers['Authorization']

        if not response.ok:
            raise EVDutyApiError(response.request_info, response.history, status=response.status, message=response.reason, headers=response.headers)
