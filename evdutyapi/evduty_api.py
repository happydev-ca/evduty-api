import aiohttp

from evdutyapi.station import Station


class EVDutyApi:
    def __init__(self, username: str, password: str, session: aiohttp.ClientSession):
        self.username = username
        self.password = password
        self.session = session
        self.session.headers.add('Content-Type', 'application/json')
        self.expires_in = None

    async def authenticate(self):
        json = {"device": {"id": "", "model": "", "type": "ANDROID"}, "email": self.username, "password": self.password}
        async with self.session.post('https://api.evduty.net/v1/account/login', json=json) as response:
            response.raise_for_status()
            body = await response.json()
            self.session.headers.add("Authorization", "Bearer " + body["accessToken"])
            self.expires_in = body["expiresIn"]

    async def async_get_stations(self):
        await self.authenticate()
        async with self.session.get('https://api.evduty.net/v1/account/stations') as response:
            response.raise_for_status()
            stations = await response.json()
            stations = [Station.from_json(s) for s in stations]
            return stations
