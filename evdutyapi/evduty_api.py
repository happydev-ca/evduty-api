import asyncio
import logging
from datetime import timedelta, datetime
from http import HTTPStatus
from logging import Logger, getLogger
from typing import List

from aiohttp import ClientResponse, ClientSession

from . import EVDutyApiError, EVDutyApiInvalidCredentialsError, Station, Terminal
from .charging_sessions.charging_session_response import ChargingSessionResponse
from .max_charging_current.max_charging_current_request import MaxChargingCurrentRequest
from .stations.station_response import StationResponse
from .terminals.terminal_response import TerminalResponse

LOGGER: Logger = getLogger(__package__)


class EVDutyApi:
    base_url = 'https://api.evduty.net'

    def __init__(self, username: str, password: str, session: ClientSession):
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
            await self._log('POST', '/v1/account/login', response, self.headers, json)
            self._raise_on_authenticate_error(response)
            body = await response.json()
            self.headers['Authorization'] = 'Bearer ' + body['accessToken']
            self.expires_at = datetime.now() + timedelta(seconds=body['expiresIn'])

    @staticmethod
    def _raise_on_authenticate_error(response: ClientResponse):
        if response.status == HTTPStatus.BAD_REQUEST:
            raise EVDutyApiInvalidCredentialsError(response)
        if not response.ok:
            raise EVDutyApiError(response)

    async def async_get_stations(self) -> List[Station]:
        async with await self._get('/v1/account/stations') as response:
            body = await response.json()
            stations = [StationResponse.from_json(station) for station in body]
            await asyncio.gather(self._async_get_terminals(stations))
            return stations

    async def _async_get_terminals(self, stations: List[Station]) -> None:
        calls = []
        for station in stations:
            for terminal in station.terminals:
                calls.append(self._async_get_terminal_details(terminal))
                calls.append(self._async_get_session(terminal))
        await asyncio.gather(*calls)

    async def _async_get_terminal_details(self, terminal: Terminal) -> None:
        async with await self._get(f'/v1/account/stations/{terminal.station_id}/terminals/{terminal.id}') as response:
            body = await response.json()
            terminal.network_info = TerminalResponse.from_json_to_network_info(body)
            terminal.charging_profile = TerminalResponse.from_json_to_charging_profile(body)

    async def _async_get_session(self, terminal: Terminal) -> None:
        async with await self._get(f'/v1/account/stations/{terminal.station_id}/terminals/{terminal.id}/session') as response:
            if await response.text() != '':
                body = await response.json()
                terminal.session = ChargingSessionResponse.from_json(body)

    async def async_set_terminal_max_charging_current(self, terminal: Terminal, current: int) -> None:
        async with await self._get(f'/v1/account/stations/{terminal.station_id}/terminals/{terminal.id}') as response:
            body = await response.json()
            request = MaxChargingCurrentRequest.from_terminal_response(body, current)
            await self._put(f'/v1/account/stations/{terminal.station_id}/terminals/{terminal.id}', json=request)

    async def async_get_monthly_report(self, year: int, month: int) -> str:
        async with await self._get(f'/v1/account/reports/owner/csv?year={year}&month={month}') as response:
            raw_body = await response.read()
            return raw_body.decode('latin-1')

    async def _get(self, url: str) -> ClientResponse:
        await self.async_authenticate()
        response = await self.session.get(f'{self.base_url}{url}', headers=self.headers)
        await self._log('GET', url, response, self.headers)
        self._raise_on_error(response)
        return response

    async def _put(self, url: str, json: dict) -> ClientResponse:
        await self.async_authenticate()
        response = await self.session.put(f'{self.base_url}{url}', headers=self.headers, json=json)
        await self._log('PUT', url, response, self.headers, json)
        self._raise_on_error(response)
        return response

    def _raise_on_error(self, response: ClientResponse):
        if response.status == HTTPStatus.UNAUTHORIZED:
            self.expires_at = datetime.now() - timedelta(seconds=1)
            del self.headers['Authorization']

        if not response.ok:
            raise EVDutyApiError(response)

    @staticmethod
    async def _log(method: str, url: str, response: ClientResponse, request_headers: dict, request_body: dict = None) -> None:
        if LOGGER.isEnabledFor(logging.DEBUG):
            request_log = f'request_headers={request_headers} request_body={request_body}'
            response_log = f'response_headers={dict(response.headers)} response_body={await response.text()}'
            LOGGER.debug(f'{response.status} {method} {url} : {request_log} {response_log}')
