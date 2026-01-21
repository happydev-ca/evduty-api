import aiohttp
import asyncio
import os

from evdutyapi import EVDutyApi


async def run():
    async with aiohttp.ClientSession() as session:
        api = EVDutyApi(os.environ['EMAIL'], os.environ['PASSWORD'], session)
        report = await api.async_get_monthly_report(2025, 12)
        print(report)


asyncio.run(run())
