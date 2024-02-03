from datetime import timedelta, datetime

import aiohttp

from evdutyapi.api_response.charging_session_response import ChargingSessionResponse
from evdutyapi.api_response.station_response import StationResponse


class EVDutyApi:
    base_url = 'https://api.evduty.net'

    def __init__(self, username: str, password: str, session: aiohttp.ClientSession):
        self.username = username
        self.password = password
        self.session = session
        self.session.headers.add('Content-Type', 'application/json')
        self.expires_at = datetime.now() - timedelta(seconds=1)

    async def async_authenticate(self):
        if datetime.now() < self.expires_at:
            return

        json = {"device": {"id": "", "model": "", "type": "ANDROID"}, "email": self.username, "password": self.password}
        async with self.session.post(f'{self.base_url}/v1/account/login', json=json) as response:
            response.raise_for_status()
            body = await response.json()
            self.session.headers.add("Authorization", "Bearer " + body["accessToken"])
            self.expires_at = datetime.now() + timedelta(seconds=body["expiresIn"])

    async def async_get_stations(self):
        await self.async_authenticate()
        async with self.session.get(f'{self.base_url}/v1/account/stations') as response:
            response.raise_for_status()
            json_stations = await response.json()
            stations = [StationResponse.from_json(s) for s in json_stations]
            await self.__async_get_sessions(stations)
            return stations

    async def __async_get_sessions(self, stations):
        for station in stations:
            for terminal in station.terminals:
                async with self.session.get(f'{self.base_url}/v1/account/stations/{station.id}/terminals/{terminal.id}/session') as response:
                    response.raise_for_status()
                    if await response.text() != "":
                        json_session = await response.json()
                        terminal.session = ChargingSessionResponse.from_json(json_session)
