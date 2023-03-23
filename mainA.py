import aiohttp
import asyncio
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

schedule = []


class Api:
    def __init__(self):
        self.api_url = os.environ.get("API_URL")

    async def get_schedule(self, params=None):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as response:
                return await response.json()


apiObj = Api()


async def start_schedule_listener():
    while True:
        data = await apiObj.get_schedule()
        print(data)
        await asyncio.sleep(1)


async def startCallsListener():
    while True:
        data = await apiObj.get_data()
        print(data)
        await asyncio.sleep(1)


async def main():
    await asyncio.gather(make_requests(api_requester1), make_requests(api_requester2))


asyncio.run(main())
