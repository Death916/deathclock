# deathclock.py (or your main app file name)

import reflex as rx
from datetime import datetime, timezone
import asyncio
import time
from rxconfig import config
# --- Import your Weather utility ---
from utils.weather import Weather

from utils.scores import NBAScores, mlbScores
from utils.news import News
# from utils.alarm import Alarm
import logging

# --- Constants ---
WEATHER_IMAGE_PATH = "/weather.jpg" # Web path in assets folder
WEATHER_FETCH_INTERVAL = 360
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class State(rx.State):

    # --- State Variables ---

    current_time: str = "" # Note: rx.moment replaces the need for this if used for display
    alarm_time: str = ""
    alarms: list = []
    news: list = [] # Placeholder
    nba_scores: list = [] # Placeholder
    mlb_scores: list = [] # Placeholder
    _news_client: News | None = None # This will be set in the constructor
    last_weather_update: str = "Never"
    weather_img: str = WEATHER_IMAGE_PATH
    _weather_client: Weather | None = None # This will be set in the constructor
    _mlb_client: list | None = None # This will be set in the constructor
    _nba_client: list | None = None # This will be set in the constructor

    # --- Initialize Utility Client ---
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize the weather client
        try:

            self._weather_client = Weather()
            self._news_client = News()
            self._mlb_client = mlbScores()
            self._nba_client = NBAScores()
            logging.info("Weather client initialized successfully.")
        except Exception as e:
            logging.error(f"Failed to initialize Weather client: {e}", exc_info=True)
            self._weather_client = None # Mark as unusable
            # Set error state if needed
            self.weather_img = "/error_placeholder.png" # Provide a placeholder error image
            self.last_weather_update = "Client Init Error"
            self.mlb_scores = ""
            self.nba_scores = ""


    # --- on_load Handler ---
    async def start_background_tasks(self):
        """Starts the weather background task when the page loads."""
        rx.remove_local_storage("chakra-ui-color-mode") #trying to test themes remove after
        logging.info("Triggering background tasks: Weather")
        # *** FIX: Return a list containing the handler reference ***
        return [State.fetch_weather, State.fetch_sports] 


    # --- Sports Background Task ---

    @rx.event(background=True)
    async def fetch_sports(self):
        

        # Fetches sports scores periodically
        while True:
            try:
                logging.info("Fetching sports scores...")
                # Fetch MLB and NBA scores
                mlb_scores = await self._mlb_client.get_scores()
                logging.info(f"MLB Scores: {mlb_scores}")
                # Check if MLB scores are empty
                if not mlb_scores:
                    logging.warning("No MLB scores fetched.")
                    async with self:
                        self.mlb_scores = []
                        yield
                nba_scores = await self._nba_client.get_scores()
                logging.info(f"NBA Scores: {nba_scores}")
                # Check if NBA scores are empty
                if not nba_scores:
                    logging.warning("No NBA scores fetched.")
                    async with self:
                        self.nba_scores = []
                        yield

                # Update state with fetched scores
                async with self:
                    self.mlb_scores = mlb_scores
                    self.nba_scores = nba_scores
                    logging.info(f"Fetched {len(mlb_scores)} MLB scores and {len(nba_scores)} NBA scores.")
                    yield  # Update frontend

            except Exception as e:
                logging.error(f"Error in fetch_sports background task: {e}", exc_info=True)
            await asyncio.sleep(500)

    # format sports scores for display
    """
        @rx.event(background=True)
        async def fetch_news(self):
            #Fetches news periodically
            # Placeholder for the actual news fetching logic
            while True:
                try:
                    logging.info("Fetching news...")
                    news_items = await self._news_client.get_news() 
                    if not news_items:
                        logging.warning("No news items fetched.")
                        async with self:
                            self.news = []
                            yield  # Update frontend
                    else:
                        logging.info(f"Fetched {len(news_items)} news items.")
                        async with self:
                            self.news = news_items
                            yield
                   
                    
                except Exception as e:
                    logging.error(f"Error in fetch_news background task: {e}", exc_info=True)
                await asyncio.sleep(500)
    
    """
    # --- Weather Background Task ---
    @rx.event(background=True)
    async def fetch_weather(self):
        """Fetches the weather screenshot periodically."""
        # Check if the client initialized correctly
        if not hasattr(self, '_weather_client') or self._weather_client is None:
            logging.warning("Weather client not initialized. Stopping fetch_weather task.")
            
            async with self:
                self.last_weather_update = "Error: Weather client unavailable"
                yield
            return # Exit the task permanently if client init failed

        while True:
            try:
                logging.info("Attempting to fetch weather screenshot...")
                # Call the method from the initialized client
                img_web_path = self._weather_client.get_weather_screenshot() 

                if img_web_path:
                    async with self:
                        timestamp = int(time.time())
                        # Update state with cache-busting query param
                        # Ensure img_web_path is like "/weather.jpg"
                        self.weather_img = f"{img_web_path}"
                        self.last_weather_update = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
                        logging.info(f"State.weather_img updated to: {self.weather_img}")
                        yield # Update frontend
                else:
                    logging.warning("get_weather_screenshot returned None. State not updated.")
                    # Optionally update status
                    async with self:
                        self.last_weather_update = f"Failed fetch @ {datetime.now(timezone.utc).strftime('%H:%M:%S UTC')}"
                        yield

            except Exception as e:
                logging.error(f"Error in fetch_weather background task: {e}", exc_info=True)
                async with self: # Update state to show error
                    self.last_weather_update = f"Error @ {datetime.now(timezone.utc).strftime('%H:%M:%S UTC')}"
                    yield

            await asyncio.sleep(WEATHER_FETCH_INTERVAL)


def index() -> rx.Component:
    
    return rx.container(
        rx.theme_panel(default_open=False),
        
        rx.center(
            rx.vstack(
                
                rx.button(
                    rx.moment(interval=1000, format="HH:mm:ss"),
                    font_size="4xl",
                    font_weight="bold",
                    color="white",
                    background_color="#6f42c1", # Original color
                 ),

                
                rx.flex(
                    rx.card(
                        rx.box(
                            rx.text("SPORTS GO HERE"), 
                        ),
                    ),
                   
                    rx.card(
                        rx.vstack( # Added vstack for title/image/status
                            rx.heading("Weather", size="4"),
                            
                            rx.image(
                                
                                src=State.weather_img,
                                alt="Current weather conditions for Sacramento",
                                width="100%", # Keep original width setting
                                height="auto", # Keep original height setting
                                
                                object_fit="contain", # Adjust fit as needed
                                border_radius="var(--radius-3)", # Use theme radius
                            ),
                            rx.text(
                                f"Last Update: {State.last_weather_update}",
                                size="1",
                                color_scheme="gray",
                                padding_top="0.5em" # Add some space
                            ),
                            align="center", # Center heading/image/text
                            spacing="2",
                        )
                    ),
                    
                    rx.card(
                        rx.box(
                            rx.text("Other sports"),
                             # Placeholder
                        ),
                    ),
                    # Original flex settings
                    spacing="3", # Add spacing between cards
                    width="100%",
                    justify="center", # Center cards horizontally
                    align="stretch", # Stretch cards vertically if needed
                ),
                
                 align="center",
                 spacing="4", # Spacing between clock and flex container
            ),
        ),
         # Original container settings
         padding="2rem", # Add some padding
         max_width="1200px", # Limit width
         margin="0 auto", # Center container
    ),

style = {
    
    "background_color": "black", # Darker purple
    "color": "#ffffff",
    "box_shadow": "0 4px 8px rgba(0, 0, 0, 0.2)",
    "transition": "background-color 0.3s ease, color 0.3s ease",
    "hover": {
        "background_color": "#3a2b4d", # Darker shade on hover
        "color": "#ffffff",
    },
    
}
app = rx.App(
    theme=rx.theme(
        appearance="dark",
        color_scheme="purple",
        accent_color="purple",
        radius="medium",
        has_background=True,
    ),
    style=style
)




app.add_page(
    index,
    title="DeathClock", # Example title
    on_load=State.start_background_tasks
     # Trigger tasks when this page loads
)

# The original TypeError is resolved by returning [State.fetch_weather]
# from State.start_background_tasks.
# The image display is fixed by binding rx.image src to State.weather_img.
