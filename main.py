"""
Auto calls
"""
import datetime
import time
import requests
import os

from dotenv import load_dotenv, find_dotenv
import playsound

load_dotenv(find_dotenv())

mp3_files = ["1.mp3", "2.mp3"]
auto_timer = ""
while True:
    timeNow = datetime.datetime.now().strftime("%H:%M")

    if auto_timer != timeNow:
        auto_timer = ""
    if auto_timer == "":
        response = requests.get(os.environ.get("API_URL") + "schedule/" + str(datetime.datetime.today().weekday()))
        if not response:
            print("API Error!!!")
        response = response.json()
        startLesson = [a for a in response if a['start'] == timeNow]
        endLesson = [a for a in response if a['end'] == timeNow]
        print(timeNow)
        if len(startLesson) != 0:
            auto_timer = timeNow
            print("Звенит звонок на урок")
            playsound.playsound(mp3_files[0], True)
        elif len(endLesson) != 0:
            auto_timer = timeNow
            print("Звенит звонок с урока")
            playsound.playsound(mp3_files[1], True)
    time.sleep(1)
