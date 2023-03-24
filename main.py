import asyncio
import concurrent.futures
import datetime
import os
import time

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
            self.lessons = await self.api_obj.get_schedule()
            await asyncio.sleep(1)

    def get_nearest_lesson(self, time_now):
        while self.lessons == []:
            time.sleep(1)
        # print(self.lessons)
        for lesson in self.lessons:
            if lesson["end"] > time_now:
                return lesson

    def get_call(self):
        time_now = self.get_time()
        nearest_call = self.get_nearest_lesson(time_now)
        while time_now not in [nearest_call["end"], nearest_call["start"]]:
            print(nearest_call, time_now)
            time.sleep(1)
        return nearest_call

    async def calls_listener(self):
        while True:
            time_now = self.get_time()
            loop = asyncio.get_running_loop()
            with concurrent.futures.ThreadPoolExecutor() as pool:
                call = await loop.run_in_executor(pool, self.get_call)
            # Действия, которые нужно выполнить при получении звонка
            print("Звонок!", call)
            await do_call(time_now in call["start"])
            await asyncio.sleep(1)

    def get_time(self):
        return datetime.datetime.now().strftime("%H:%M")
    #
    # async def start_calls_listener(self):
    #     auto_timer = ""
    #
    #     while True:
    #         time_now = datetime.datetime.now().strftime("%H:%M")
    #
    #         print(time_now)
    #         print(self.schedule)
    #
    #         if auto_timer != time_now:
    #             auto_timer = ""
    #
    #         if auto_timer == "":
    #             start_lesson = [a for a in self.schedule if a['start'] == time_now]
    #             end_lesson = [a for a in self.schedule if a['end'] == time_now]
    #
    #             if len(start_lesson) != 0:
    #                 auto_timer = time_now
    #                 print("Звенит звонок на урок")
    #                 await play_sound(MP3_FILES[0])
    #             elif len(end_lesson) != 0:
    #                 auto_timer = time_now
    #                 print("Звенит звонок с урока")
    #                 await play_sound(MP3_FILES[1])
    #         await asyncio.sleep(1)


listener = Listeners()
# if __name__ == "__main__":
#     api = Api()
#     loop = asyncio.get_event_loop()
#     print(loop.run_until_complete(api.get_schedule()))
