# /home/death916/code/python/deathclock/utils/weather.py
import datetime
import logging  # Optional: Use logging for better error messages
import os
import subprocess

import reflex as rx

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Define the target filename consistently
WEATHER_FILENAME = "weather.jpg"
# Define the web path expected by the frontend
WEATHER_WEB_PATH = f"/{WEATHER_FILENAME}"  # This should be relative to the assets dir


class Weather(rx.Base):
    def _get_assets_dir(self) -> str:
        """Calculates and ensures the assets directory exists within the project."""

        script_dir = os.path.dirname(os.path.abspath(__file__))

        project_root = os.path.dirname(script_dir)
        assets_dir = os.path.join(project_root, "assets")

        # Ensure the assets directory exists
        if not os.path.exists(assets_dir):
            try:
                os.makedirs(assets_dir)
                logging.info(f"Created assets directory: {assets_dir}")
            except OSError as e:
                logging.error(f"Failed to create assets directory {assets_dir}: {e}")
        return assets_dir

    def delete_old_screenshots(self, assets_dir: str):
        """Deletes the specific weather file in the given 'assets' directory."""
        target_file = os.path.join(assets_dir, WEATHER_FILENAME)
        if os.path.exists(target_file):
            try:
                os.remove(target_file)
                logging.info(f"Deleted old weather file: {target_file}")
            except OSError as e:
                logging.error(f"Failed to delete old weather file {target_file}: {e}")

    def get_weather_screenshot(self) -> str | None:
        """
        Fetches weather info using curl, saves it to the project's assets dir.
        Returns the web path (e.g., '/weather.jpg') or None on failure.
        """
        assets_dir = self._get_assets_dir()
        screenshot_path = os.path.join(assets_dir, WEATHER_FILENAME)

        try:
            curl_command = [
                "curl",
                "-s",  # Silent mode
                "v2.wttr.in/Sacramento.png?0u",  # Fetch PNG, no border, no terminal escapes
                "-o",
                screenshot_path,  # Save to the correct assets path
            ]

            # Delete the old file before creating the new one
            self.delete_old_screenshots(assets_dir)

            logging.info(
                f"Running curl command to fetch weather: {' '.join(curl_command)}"
            )
            logging.info(
                f"Curl command successful. Weather image saved to: {screenshot_path}"
            )  # Log correct save path

            return WEATHER_WEB_PATH

        except subprocess.CalledProcessError as e:
            logging.error(f"Curl command failed for path {screenshot_path}: {e}")
            logging.error(f"Curl stderr: {e.stderr}")
            return None
        except Exception as e:
            logging.error(
                f"An unexpected error occurred saving to {screenshot_path}: {e}"
            )
            return None
