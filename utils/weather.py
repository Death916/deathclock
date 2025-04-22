# /home/death916/code/python/deathclock/utils/weather.py
import os
import subprocess
import datetime
import reflex as rx
import logging # Optional: Use logging for better error messages

# Configure logging (optional but recommended)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the target filename consistently
WEATHER_FILENAME = "weather.jpg"
# Define the web path expected by the frontend
WEATHER_WEB_PATH = f"/{WEATHER_FILENAME}" # This should be relative to the assets dir

class Weather(rx.Base):
    # No __init__ needed here for Pydantic compatibility

    def _get_assets_dir(self) -> str:
        """Calculates and ensures the assets directory exists within the project."""
        # Get the directory where this script (weather.py) is located
        # e.g., /home/death916/code/python/deathclock/utils
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the absolute path to the project root directory
        # This should be the parent directory of 'utils'
        # e.g., /home/death916/code/python/deathclock
        # --- FIX IS HERE ---
        project_root = os.path.dirname(script_dir)
        # -----------------

        # Construct the absolute path to the 'assets' directory within the project root
        # e.g., /home/death916/code/python/deathclock/assets
        assets_dir = os.path.join(project_root, 'assets')

        # Ensure the assets directory exists
        if not os.path.exists(assets_dir):
            try:
                os.makedirs(assets_dir)
                logging.info(f"Created assets directory: {assets_dir}")
            except OSError as e:
                logging.error(f"Failed to create assets directory {assets_dir}: {e}")
                # If directory creation fails, saving will also likely fail.
                # Consider raising an exception or returning None early.
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
        # If _get_assets_dir failed (e.g., couldn't create dir), it might be None or invalid.
        # Adding a check here could be useful, though currently it returns the path anyway.
        # if not assets_dir or not os.path.isdir(assets_dir):
        #    logging.error("Assets directory path is invalid or missing.")
        #    return None

        # Full path to save the file, e.g., /home/death916/code/python/deathclock/assets/weather.jpg
        screenshot_path = os.path.join(assets_dir, WEATHER_FILENAME)

        try:
            curl_command = [
                "curl",
                "-s",  # Silent mode
                "v2.wttr.in/Sacramento.png?0T", # Fetch PNG, no border, no terminal escapes
                "-o",
                screenshot_path, # Save to the correct assets path
            ]

            # Delete the old file before creating the new one
            self.delete_old_screenshots(assets_dir)

            logging.info(f"Running curl command to fetch weather: {' '.join(curl_command)}")
            process = subprocess.run(curl_command, check=True, capture_output=True, text=True)
            logging.info(f"Curl command successful. Weather image saved to: {screenshot_path}") # Log correct save path

            # *** Return the WEB PATH, which is relative to the assets dir ***
            # This part was already correct. Reflex serves the 'assets' folder at the root URL.
            return WEATHER_WEB_PATH # e.g., "/weather.jpg"

        except subprocess.CalledProcessError as e:
            logging.error(f"Curl command failed for path {screenshot_path}: {e}")
            logging.error(f"Curl stderr: {e.stderr}")
            return None
        except Exception as e:
            logging.error(f"An unexpected error occurred saving to {screenshot_path}: {e}")
            return None