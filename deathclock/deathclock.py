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
    """The app state."""



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
                rx.card(
                    rx.image(
                        src="/weather.jpg",  # Use relative path to static asset
                        alt="Weather",
                        width="100%",
                        height="auto",
                        background_color="white",
                    ),
                ),
            ),
        ),    
    ),           
                   

        
            

        
    

        
  


app = rx.App()
app.add_page(index)
