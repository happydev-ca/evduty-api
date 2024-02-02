import aiohttp


class EVDutyApi:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = aiohttp.ClientSession()
        self.session.headers.add('Content-Type', 'application/json')
        self.expires_in = None

    async def __aenter__(self):
        await self.session.__aenter__()
        return self

    async def __aexit__(self, *args):
        await self.session.__aexit__(*args)

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
            return stations
