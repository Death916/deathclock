# deathclock.py (or your main app file name)

import reflex as rx
from datetime import datetime, timezone
import asyncio
import time
# Remove rxconfig import if not used directly
# from rxconfig import config
# --- Import your Weather utility ---
from utils.weather import Weather

# from utils.scores import NBAScores, mlbScores
# from utils.news import News
# from utils.alarm import Alarm
import logging

# --- Constants ---
WEATHER_IMAGE_PATH = "/weather.jpg" # Web path in assets folder
WEATHER_FETCH_INTERVAL = 360
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class State(rx.State):

    # --- Original state variables (kept as requested) ---
    current_time: str = "" # Note: rx.moment replaces the need for this if used for display
    alarm_time: str = ""
    alarms: list = []
    news: list = [] # Placeholder
    nba_scores: str = "" # Placeholder
    mlb_scores: str = "" # Placeholder

    # --- Weather-specific state variables ---
    last_weather_update: str = "Never"
    # Initialize with the base path, it will be updated with cache-buster
    weather_img: str = WEATHER_IMAGE_PATH
    # Placeholder for the weather client
    _weather_client: Weather | None = None # This will be set in the constructor

    # --- Initialize Utility Client ---
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize the weather client
        try:
           
            self._weather_client = Weather()
            logging.info("Weather client initialized successfully.")
        except Exception as e:
            logging.error(f"Failed to initialize Weather client: {e}", exc_info=True)
            self._weather_client = None # Mark as unusable
            # Set error state if needed
            self.weather_img = "/error_placeholder.png" # Provide a placeholder error image
            self.last_weather_update = "Client Init Error"


    # --- on_load Handler ---
    async def start_background_tasks(self):
        """Starts the weather background task when the page loads."""
        logging.info("Triggering background tasks: Weather")
        # *** FIX: Return a list containing the handler reference ***
        return [State.fetch_weather]

    # --- Weather Background Task ---
    @rx.event(background=True)
    async def fetch_weather(self):
        """Fetches the weather screenshot periodically."""
        # Check if the client initialized correctly
        if not hasattr(self, '_weather_client') or self._weather_client is None:
            logging.warning("Weather client not initialized. Stopping fetch_weather task.")
            # Optionally update state to reflect this persistent error
            async with self:
                self.last_weather_update = "Error: Weather client unavailable"
                yield
            return # Exit the task permanently if client init failed

        while True:
            try:
                logging.info("Attempting to fetch weather screenshot...")
                # Call the method from the initialized client
                img_web_path = self._weather_client.get_weather_screenshot() # This now comes from utils/weather.py

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
                    # Optionally reset image to placeholder on error
                    # self.weather_img = WEATHER_IMAGE_PATH
                    yield

            await asyncio.sleep(WEATHER_FETCH_INTERVAL)


def index() -> rx.Component:
    """ Main UI definition, preserving original structure. """
    return rx.container(
        rx.center(
            rx.vstack(
                # Original Clock Button
                rx.button(
                    rx.moment(interval=1000, format="HH:mm:ss"),
                    font_size="4xl",
                    font_weight="bold",
                    color="white",
                    background_color="#6f42c1", # Original color
                 ),

                # Original Flex Layout for Cards
                rx.flex(
                    rx.card(
                        rx.box(
                            rx.text("SPORTS GO HERE"), # Placeholder
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
                            rx.text("Other sports"), # Placeholder
                        ),
                    ),
                    # Original flex settings
                    spacing="3", # Add spacing between cards
                    width="100%",
                    justify="center", # Center cards horizontally
                    align="stretch", # Stretch cards vertically if needed
                ),
                # Original vstack settings
                 align="center",
                 spacing="4", # Spacing between clock and flex container
            ),
        ),
         # Original container settings
         padding="2rem", # Add some padding
         max_width="1200px", # Limit width
         margin="0 auto", # Center container
    ),


# --- App Setup ---
app = rx.App(
    theme=rx.theme(
        appearance="dark", # Use dark theme
        accent_color="purple",
        radius="medium", # Apply consistent border radius
    )
)


app.add_page(
    index,
    title="DeathClock", # Example title
    on_load=State.start_background_tasks # Trigger tasks when this page loads
)

# The original TypeError is resolved by returning [State.fetch_weather]
# from State.start_background_tasks.
# The image display is fixed by binding rx.image src to State.weather_img.