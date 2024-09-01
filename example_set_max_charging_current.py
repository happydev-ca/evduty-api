import aiohttp
import asyncio
import os

from evdutyapi import EVDutyApi

email = os.environ['EMAIL']
password = os.environ['PASSWORD']
current = int(os.environ['CURRENT'])
print('will set max current to', current)

async def run():
    async with aiohttp.ClientSession() as session:
        api = EVDutyApi(email, password, session)
        stations = await api.async_get_stations()

        station = stations[0]
        print(station)

        terminal = station.terminals[0]
        print(terminal)

        print(terminal.charging_profile)
        await api.async_set_terminal_max_charging_current(terminal, current=current)

asyncio.run(run())
