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

        terminal = await get_first_terminal(api)
        print(terminal.charging_profile)

        await api.async_set_terminal_max_charging_current(terminal, current=current)

        terminal = await get_first_terminal(api)
        print(terminal.charging_profile)


async def get_first_terminal(api):
    stations = await api.async_get_stations()
    station = stations[0]
    terminal = station.terminals[0]
    return terminal


asyncio.run(run())
