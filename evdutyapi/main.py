import asyncio
import os

from evdutyapi import EVDutyApi


async def run():
    async with EVDutyApi(os.environ['EMAIL'], os.environ['PASSWORD']) as api:
        stations = await api.async_get_stations()
        for station in stations:
            print("station:  " + station["id"])
            for terminal in station["terminals"]:
                print("terminal: " + terminal["id"], terminal["status"])


asyncio.run(run())
