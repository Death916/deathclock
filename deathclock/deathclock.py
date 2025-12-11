# deathclock.py
import asyncio

# from utils.alarm import Alarm # Commented out import
import logging
import time
from datetime import datetime, timezone
from typing import Any, Dict, List

import reflex as rx

_background_tasks_registered = False

from utils.news import News
from utils.radio import Radio
from utils.scores import NBAScores, mlbScores, nflScores
from utils.weather import Weather

WEATHER_IMAGE_PATH = "/weather.jpg"  # Web path in assets folder
WEATHER_FETCH_INTERVAL = 360
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class State(rx.State):
    # --- State Variables ---

    current_time: str = ""
    alarm_time: str = ""
    alarms: List = []
    news: List[Dict[str, Any]] = []
    current_news_index: int = 0
    news_rotate_interval: int = 10
    news_text: str = ""
    nba_scores: List[Dict[str, Any]] = []
    mlb_scores: List[Dict[str, Any]] = []
    nfl_scores: List[Dict[str, Any]] = []
    radio_stations: List[str] = []
    current_radio_station: str = ""
    _news_client: News | None = None  # This will be set in the constructor
    last_weather_update: str = "Never"
    weather_img: str = WEATHER_IMAGE_PATH
    _weather_client: Weather | None = None  # This will be set in the constructor
    _mlb_client: mlbScores | None = None
    _nba_client: NBAScores | None = None
    _nfl_client: nflScores | None = None
    _radio_client: Radio = Radio()
    last_sports_update: float = 0.0
    last_weather_fetch_time: float = 0.0

    # --- Initialize Utility Client ---
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize background clients
        try:
            self._weather_client = Weather()
            self._news_client = News()
            self._mlb_client = mlbScores()
            self._nba_client = NBAScores()
            self._nfl_client = nflScores()
            self._radio_client = Radio()

            logging.info("Weather client initialized successfully.")
        except Exception as e:
            logging.error(f"Failed to initialize Weather client: {e}", exc_info=True)
            self._weather_client = None
            # Set error state if needed
            self.weather_img = "/error_placeholder.png"
            self.last_weather_update = "Client Init Error"
            self.mlb_scores = []
            self.nba_scores = []
            self.last_sports_update = 0.0

    # --- on_load Handler ---
    async def start_background_tasks(self):
        global _background_tasks_registered
        """Starts the weather background task when the page loads."""
        rx.remove_local_storage("chakra-ui-color-mode")
        if _background_tasks_registered:
            logging.info(
                "Background tasks already registered in this process; skipping."
            )
            return []
        _background_tasks_registered = True
        logging.info("Triggering background tasks: Weather")
        return [
            State.fetch_weather,
            State.fetch_sports,
            State.fetch_news,
            State.cycle_news,
        ]

    @rx.event(background=True)
    async def fetch_sports(self):
        # Fetches sports scores periodically
        while True:
            try:
                logging.info("Fetching sports scores...")
                # Fetch MLB and NBA scores
                # check if sports has updated in last 5 minutes if so skip
                if (
                    self.last_sports_update
                    and (time.time() - self.last_sports_update) < 300
                ):
                    logging.info(
                        "Sports scores already updated within the last 5 minutes. Skipping fetch."
                    )
                    await asyncio.sleep(300)
                    continue

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
                nfl_scores = await self._nfl_client.get_scores()
                logging.info(f"NFL Scores: {nfl_scores}")
                # Check if NFL scores are empty
                if not nfl_scores:
                    logging.warning("No NFL scores fetched.")
                    async with self:
                        self.nfl_scores = []
                        yield
                # Update state with fetched scores
                async with self:
                    self.mlb_scores = mlb_scores
                    self.nba_scores = nba_scores
                    self.nfl_scores = nfl_scores
                    self.last_sports_update = (
                        time.time()
                    )  # Update last sports update time
                    logging.info(
                        f"Fetched {len(mlb_scores)} MLB scores and {len(nba_scores)} NBA scores and {len(nfl_scores)} NFL scores."
                    )
                    yield  # Update frontend

            except Exception as e:
                logging.error(
                    f"Error in fetch_sports background task: {e}", exc_info=True
                )
            await asyncio.sleep(500)

    @rx.event(background=True)
    async def fetch_news(self):
        while True:
            try:
                logging.info("Fetching news...")
                news_items = await self._news_client.get_news()
                if not news_items:
                    logging.warning("No news items fetched.")
                    async with self:
                        self.news = []
                        self.current_news_index = 0
                        yield
                else:
                    logging.info(f"Fetched {len(news_items)} news items.")
                    async with self:
                        self.news = news_items
                        self.current_news_index = 0
                        yield

            except Exception as e:
                logging.error(
                    f"Error in fetch_news background task: {e}", exc_info=True
                )
            await asyncio.sleep(500)

    @rx.event(background=True)
    async def cycle_news(self):
        while True:
            try:
                if self.news:
                    async with self:
                        self.current_news_index = (self.current_news_index + 1) % len(
                            self.news
                        )
                        yield
            except Exception as e:
                logging.error(
                    f"Error in cycle_news background task: {e}", exc_info=True
                )
            await asyncio.sleep(self.news_rotate_interval)

    # --- Weather Background Task ---
    @rx.event(background=True)
    async def fetch_weather(self):
        """Fetches the weather screenshot periodically."""
        if not hasattr(self, "_weather_client") or self._weather_client is None:
            logging.warning(
                "Weather client not initialized. Stopping fetch_weather task."
            )

            async with self:
                self.last_weather_update = "Error: Weather client unavailable"
                yield
            return

        while True:
            try:
                if (
                    self.last_weather_fetch_time
                    and (time.time() - self.last_weather_fetch_time)
                    < WEATHER_FETCH_INTERVAL
                ):
                    logging.info(
                        "Recent weather fetch detected; skipping immediate fetch to avoid thrashing."
                    )
                    await asyncio.sleep(WEATHER_FETCH_INTERVAL)
                    continue
                logging.info("deleting existing weather screenshot...")
                self._weather_client.delete_old_screenshots(self.weather_img)
                logging.info("Attempting to fetch weather screenshot...")

                img_web_path = self._weather_client.get_weather_screenshot()

                if img_web_path:
                    async with self:
                        self.weather_img = f"{img_web_path}"
                        self.last_weather_update = datetime.now(timezone.utc).strftime(
                            "%Y-%m-%d %H:%M:%S UTC"
                        )
                        self.last_weather_fetch_time = time.time()
                        logging.info(
                            f"State.weather_img updated to: {self.weather_img}"
                        )
                        yield

                else:
                    logging.warning(
                        "get_weather_screenshot returned None. State not updated."
                    )
                    async with self:
                        self.last_weather_update = f"Failed fetch @ {datetime.now(timezone.utc).strftime('%H:%M:%S UTC')}"
                        yield

            except Exception as e:
                logging.error(
                    f"Error in fetch_weather background task: {e}", exc_info=True
                )
                async with self:
                    self.last_weather_update = (
                        f"Error @ {datetime.now(timezone.utc).strftime('%H:%M:%S UTC')}"
                    )
                    yield
            logging.info("Weather fetch completed")
            logging.info("Sleeping for next fetch")
            await asyncio.sleep(WEATHER_FETCH_INTERVAL)


def index() -> rx.Component:
    # Build NBA scores list (safe access with .get where appropriate)
    nba_scores_list = rx.box(
        rx.vstack(
            rx.foreach(
                State.nba_scores,
                lambda score: rx.card(
                    rx.text(
                        f"{score.get('away_team', '?')} {score.get('away_score', '-')} @ "
                        f"{score.get('home_team', '?')} {score.get('home_score', '-')}  "
                        f"(Status: {score.get('status', '?')})",
                        size="1",
                    ),
                    width="100%",
                    padding="0.5",
                    variant="surface",
                ),
            ),
            spacing="1",
            align_items="stretch",
            width="auto",
        ),
        max_height="60vh",
        overflow_y="auto",
        padding="0.25rem",
    )

    nba_card = rx.card(
        rx.box(
            rx.text("NBA Scores"),
            nba_scores_list,
        ),
        width="auto",
        padding="1",
    )

    # Weather card
    weather_card = rx.card(
        rx.vstack(
            rx.heading("Weather", size="4"),
            rx.image(
                src=State.weather_img,
                alt="Current weather conditions for Sacramento",
                width="100%",
                height="60vh",
                object_fit="contain",
                border_radius="var(--radius-3)",
                padding_top="0",
                padding_bottom="0",
            ),
            rx.text(
                f"Last Update: {State.last_weather_update}",
                size="1",
                color_scheme="gray",
                padding_top="0",
            ),
            align="center",
            spacing="2",
        )
    )

    # MLB scores list
    mlb_scores_list = rx.vstack(
        rx.foreach(
            State.mlb_scores,
            lambda score: rx.card(
                rx.text(
                    f"{score.get('away_team', '?')} {score.get('away_score', '-')} @ "
                    f"{score.get('home_team', '?')} {score.get('home_score', '-')}  "
                    f"({score.get('status', '?')})",
                    size="1",
                ),
                size="1",
                padding="1",
                variant="surface",
                width="100%",
            ),
        ),
        spacing="1",
        align_items="stretch",
        width="100%",
    )

    mlb_card = rx.card(
        rx.box(
            rx.text("MLB Scores"),
            mlb_scores_list,
        )
    )

    nfl_scores_list = rx.vstack(
        rx.foreach(
            State.nfl_scores,
            lambda score: rx.card(
                rx.text(
                    f"{score.get('away_team', '?')} {score.get('away_score', '-')} @ "
                    f"{score.get('home_team', '?')} {score.get('home_score', '-')}  "
                    f"({score.get('status', '?')})",
                    size="1",
                ),
                size="1",
                padding="1",
                variant="surface",
                width="100%",
            ),
        ),
        spacing="1",
        align_items="stretch",
        width="100%",
    )

    nfl_card = rx.card(
        rx.box(
            rx.text("NFL Scores"),
            nfl_scores_list,
        )
    )

    # Main flexible content area
    main_flex = rx.flex(
        nba_card,
        weather_card,
        rx.vstack(
            mlb_card,
            nfl_card,
        ),
        spacing="2",
        width="100%",
        justify="center",
        align="baseline",
    )

    # Top clock button
    clock_button = rx.button(
        rx.moment(interval=1000, format="HH:mm:ss"),
        font_size="4xl",
        font_weight="bold",
        color="white",
        background_color="#6f42c1",
    )

    news_card = rx.card(
        rx.box(
            rx.center(
                rx.text("News Headlines"),
            ),
            rx.center(
                rx.cond(
                    State.news,
                    rx.text(
                        rx.heading(State.news[State.current_news_index]["source"]),
                        rx.spacer(),
                        State.news[State.current_news_index]["title"],
                        rx.spacer(),
                        State.news[State.current_news_index]["publish_date"],
                        font_size="lg",
                        color="gray.500",
                        no_of_lines=1,
                        white_space="nowrap",
                        overflow="hidden",
                        text_overflow="ellipsis",
                    ),
                    rx.text(
                        "No news available",
                        font_size="lg",
                        color="gray.500",
                    ),
                ),
                width="100%",
                min_height="3.25rem",
            ),
            padding="2",
        ),
        variant="surface",
        width="100%",
    )

    # Compose the page
    page = rx.container(  # pyright: ignore[reportReturnType]
        rx.theme_panel(default_open=False),
        rx.flex(
            rx.vstack(
                rx.hstack(
                    State._radio_client.radio_card(),
                    clock_button,
                ),
                main_flex,
                news_card,
                align="center",
                spacing="2",
            )
        ),
        padding="2rem",
        max_width="800px",
        max_height="300px",
        margin="0 auto",
        flex_direction="column",
    )

    return page


""" # Commented out style block
style = {

    "background_color": "black",
    "color": "#ffffff",
    "box_shadow": "0 4px 8px rgba(0, 0, 0, 0.2)",
    "transition": "background-color 0.3s ease, color 0.3s ease",
    "hover": {
        "background_color": "#3a2b4d",
        "color": "#ffffff",
    },
}
"""
app = rx.App(
    theme=rx.theme(
        appearance="dark",
        color_scheme="purple",
        accent_color="purple",
        radius="medium",
        gray_color="mauve",
        has_background=True,
    ),
    # style=style # using theme instead
)


app.add_page(
    index,
    title="DeathClock",
    on_load=State.start_background_tasks,  # Trigger tasks when this page loads
)
