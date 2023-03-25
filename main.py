import asyncio
import datetime
import os

import aiohttp
from dotenv import load_dotenv, find_dotenv
from playsound import playsound

load_dotenv(find_dotenv())

MP3_FILES = ["1.mp3", "2.mp3"]
AUTO_TIMER = ""
API_URL = os.environ.get("API_URL")


class Api:
    def __init__(self):
        self.url = API_URL

    async def get_schedule(self):
        async with aiohttp.ClientSession() as session:
            day = str(datetime.datetime.today().weekday())
            async with session.get(self.url + "schedule/" + day) as response:
                return await response.json()


class Listeners:
    def __init__(self):
        self.lessons = []
        self.api_obj = Api()
        self.time = ""
        asyncio.run(self.start())

    async def update_time(self):
        self.time = datetime.datetime.now().strftime("%H:%M")

    async def start(self):
        await self.update_time()
        await asyncio.gather(self.schedule_listener(), self.calls_listener())

    async def schedule_listener(self):
        while True:
            data = await self.api_obj.get_schedule()
            self.lessons = sorted(data, key=lambda lesson: lesson["start"])
            await asyncio.sleep(1)

    async def get_nearest_lesson(self):
        while not self.lessons:
            await asyncio.sleep(1)

        await self.update_time()

        for lesson in self.lessons:
            if lesson["end"] >= self.time:
                return lesson

    async def get_call(self):
        await self.update_time()
        nearest_call = await self.get_nearest_lesson()

        if nearest_call == None:
            return []

        while self.time not in [nearest_call["end"], nearest_call["start"]]:
            await self.update_time()
            await asyncio.sleep(1)

        return nearest_call

    async def calls_listener(self):
        while True:
            await self.update_time()

            call = await self.get_call()

            if call == []:
                continue

            call_type = 1
            if self.time in call["start"]:
                call_type = 0

            call_exec = self.time

            await self.do_call(call_type)

            while call_exec == self.time:
                await self.update_time()
                await asyncio.sleep(1)

            await asyncio.sleep(1)

    async def do_call(self, type):
        print("Звонок", type)
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, playsound, MP3_FILES[type])


listener = Listeners()
