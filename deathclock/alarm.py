#alarm.py
# alarm component for dash app

from dash import html, dcc
import datetime
import time

class Alarm:
    def __init__(self):
        self.current_time = datetime.datetime.now()
        self.alarms = []
        self.alarm_times = []


    def add_alarm(self, alarm_time,current_time):
        self.alarms.append(alarm_time)
        self.alarm_times.append(alarm_time.time())
        self.current_time = current_time

        print(f"Alarm set for {alarm_time}")

    def check_alarm(self):
        current_time = datetime.datetime.now()
        if current_time.time() in self.alarm_times:
            print("Alarm triggered!")
            return True
        return False

