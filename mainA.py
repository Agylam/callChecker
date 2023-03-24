import aiohttp
import asyncio
import datetime
import os
from playsound import playsound
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

schedule = []
MP3_FILES = ["1.mp3", "2.mp3"]
auto_timer = ""

class Api:
    def __init__(self):
        self.url = os.environ.get("API_URL")

    async def get_schedule(self):
        async with aiohttp.ClientSession() as session:
            dof = await get_dof()
            async with session.get(self.url+"schedule/"+dof) as response:
                return await response.json()


apiObj = Api()


async def get_dof():
    return str(datetime.datetime.today().weekday())

async def start_schedule_listener():
    while True:
        global schedule, auto_timer
        schedule = await apiObj.get_schedule()
        await asyncio.sleep(20)

async def startCallsListener():
    global schedule
    auto_timer = ""
    while True:
        print(schedule)
        timeNow = datetime.datetime.now().strftime("%H:%M")
        if auto_timer != timeNow:
            auto_timer = ""
        if auto_timer == "":
            startLesson = [a for a in schedule if a['start'] == timeNow]
            endLesson = [a for a in schedule if a['end'] == timeNow]
            print(timeNow)
            if len(startLesson) != 0:
                auto_timer = timeNow
                print("Звенит звонок на урок")
                await play_sound(MP3_FILES[0])
            elif len(endLesson) != 0:
                auto_timer = timeNow
                print("Звенит звонок с урока")
                await play_sound(MP3_FILES[1])
        await asyncio.sleep(1)

async def play_sound(file_path):
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, playsound, file_path)

async def main():
    await asyncio.gather(start_schedule_listener(), startCallsListener())


asyncio.run(main())
