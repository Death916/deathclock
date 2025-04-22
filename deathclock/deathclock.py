"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from datetime import datetime, timezone
import asyncio

from rxconfig import config
from utils.weather import Weather
from utils.scores import NBAScores, mlbScores
from utils.news import News
from utils.alarm import Alarm

class State(rx.State):
    def __init__(self):
        self.weather = Weather()
        self.nbaScores = NBAScores()
        self.mlbScores = mlbScores()
        self.news = News()

    # Define the state variables
    current_time: str = ""
    last_weather_update: str = ""
    alarm_time: str = ""
    alarms: list = []
    weather_img: str = ""
    news: list = []
    nba_scores: str = ""
    mlb_scores: str = ""

    def get_weather(self):
    
        @rx.background
        async def fetch_weather():
            while True:
                async with self:
                    weather_img = self.weather.get_weather_screenshot()
                    self.weather_img = weather_img
                    print(f"Weather image updated: {weather_img}")
                    yield
                await asyncio.sleep(180)  # Fetch every 60 seconds
                

    

def index() -> rx.Component:
    
    return rx.container(
        rx.center(
            rx.vstack(
                rx.button(
                    rx.moment(interval=1000, format="HH:mm:ss"),
                    font_size="4xl",
                    font_weight="bold",
                    color="white",
                    background_color="#6f42c1",
                 ),
                    

                rx.flex(
                    rx.card(
                        rx.box(
                            rx.text("SPORTS GO HERE"),
                        ),

                    ),
                    rx.card(
                        rx.image(
                            src="/weather.jpg",  # Use relative path to static asset
                            alt="Weather",
                            width="100%",
                            height="auto",
                            background_color="white",
                            
                        ),
                   
                    ),
                    rx.card(
                        rx.box(
                            rx.text("Other sports"),
                        ),
                    ),
                    
                )
                
            ),
        ),    
    ),           
                   

        

app = rx.App()
app.add_page(index)
