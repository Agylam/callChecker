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


class Api:
    def __init__(self):
        self.url = os.environ.get("API_URL")

    async def get_schedule(self):
        async with aiohttp.ClientSession() as session:
            dof = await get_dof()
            async with session.get(self.url + "schedule/" + dof) as response:
                return await response.json()


async def get_dof():
    return str(datetime.datetime.today().weekday())


async def play_sound(file_path):
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, playsound, file_path)


class Listeners:
    def __init__(self):
        self.schedule = []
        self.api_obj = Api()
        asyncio.run(self.start())

    async def start(self):
        await asyncio.gather(self.start_schedule_listener(), self.start_calls_listener())

    async def start_schedule_listener(self):
        while True:
            self.schedule = await self.api_obj.get_schedule()
            await asyncio.sleep(20)

    async def start_calls_listener(self):
        auto_timer = ""
        while True:
            time_now = datetime.datetime.now().strftime("%H:%M")
            print(time_now)
            print(self.schedule)
            if auto_timer != time_now:
                auto_timer = ""
            if auto_timer == "":
                start_lesson = [a for a in self.schedule if a['start'] == time_now]
                end_lesson = [a for a in self.schedule if a['end'] == time_now]
                if len(start_lesson) != 0:
                    auto_timer = time_now
                    print("Звенит звонок на урок")
                    await play_sound(MP3_FILES[0])
                elif len(end_lesson) != 0:
                    auto_timer = time_now
                    print("Звенит звонок с урока")
                    await play_sound(MP3_FILES[1])
            await asyncio.sleep(1)


listener = Listeners()
