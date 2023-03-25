import asyncio
import datetime
import os

import aiohttp
from dotenv import load_dotenv, find_dotenv
from playsound import playsound

load_dotenv(find_dotenv())

schedule = []
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


async def do_call(type):
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, playsound, MP3_FILES[type])


class Listeners:
    def __init__(self):
        self.lessons = []
        self.api_obj = Api()
        asyncio.run(self.start())

    async def start(self):
        await asyncio.gather(self.schedule_listener(), self.calls_listener())

    async def schedule_listener(self):
        while True:
            data = await self.api_obj.get_schedule()
            self.lessons = sorted(data, key=lambda lesson: lesson["start"])
            await asyncio.sleep(1)

    async def get_nearest_lesson(self):
        while self.lessons == []:
            await asyncio.sleep(1)

        time_now = datetime.datetime.now().strftime("%H:%M")

        for lesson in self.lessons:
            if lesson["end"] >= time_now:
                return lesson

    # Функция для получения ближайшего звонка
    async def get_call(self):
        time_now = datetime.datetime.now().strftime("%H:%M")
        nearest_call = await self.get_nearest_lesson()

        if nearest_call == []:
            return []

        while time_now not in [nearest_call["end"], nearest_call["start"]]:
            time_now = datetime.datetime.now().strftime("%H:%M")

            await asyncio.sleep(1)

        return nearest_call

    async def calls_listener(self):
        while True:
            time_now = datetime.datetime.now().strftime("%H:%M")
            call = await self.get_call()
            if call == []:
                continue
            if time_now in call["start"]:
                call_type = 0
            else:
                call_type = 1

            call_exec = time_now

            print("Звонок", call, call_type)
            await do_call(call_type)

            while call_exec == time_now:
                time_now = datetime.datetime.now().strftime("%H:%M")
                await asyncio.sleep(1)

            await asyncio.sleep(1)


listener = Listeners()
