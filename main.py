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
                print("return Request")
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
            print("Before API Request")
            data = await self.api_obj.get_schedule()
            print("After API Request:", data)
            self.lessons = sorted(data, key=lambda lesson: lesson["start"])
            await asyncio.sleep(1)

    async def get_nearest_lesson(self):
        while self.lessons == []:
            print("Waiting for lessons")
            await asyncio.sleep(1)
        time_now = datetime.datetime.now().strftime("%H:%M")
        print("NaerLes NowTime:", time_now)
        for lesson in self.lessons:
            if lesson["end"] > time_now:
                return lesson

    # Функция для получения ближайшего звонка
    async def get_call(self):
        time_now = datetime.datetime.now().strftime("%H:%M")
        nearest_call = await self.get_nearest_lesson()
        print("NC:", nearest_call)
        while time_now not in [nearest_call["end"], nearest_call["start"]]:
            time_now = datetime.datetime.now().strftime("%H:%M")
            print("Waiting nearest call... Time_Now:", time_now)
            await asyncio.sleep(1)
        return nearest_call

    async def calls_listener(self):
        # Запуск функцции получения звонка
        while True:
            print("Before get_call")
            call = await self.get_call()
            print("After get_call")
            print("Звонок", call)
            await asyncio.sleep(1)
            # Действия, которые нужно выполнить при получении звонка

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
