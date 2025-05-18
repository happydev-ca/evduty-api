import aiohttp
import asyncio
import os

from evdutyapi import EVDutyApi


async def run():
    async with aiohttp.ClientSession() as session:
        api = EVDutyApi(os.environ['EMAIL'], os.environ['PASSWORD'], session)
        stations = await api.async_get_stations()
        for station in stations:
            print(station)

asyncio.run(run())
