import os
import subprocess
import datetime

class Weather:
    def __init__(self):
        # Get the directory where this script (weather.py) is located
        self.script_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the absolute path to the 'assets' directory in the same directory as the script
        self.assets_dir = os.path.join(self.script_dir, 'assets')

        # Ensure the assets directory exists
        if not os.path.exists(self.assets_dir):
            os.makedirs(self.assets_dir)
    
    def delete_old_screenshots(self):
        """
        Deletes all PNG files in the 'assets' directory that start with 'sacramento_weather_'.
        """
        for filename in os.listdir(self.assets_dir):
            if filename.startswith("sacramento_weather_"):
                os.remove(os.path.join(self.assets_dir, filename))

    def get_weather_screenshot(self):
        """
        Fetches weather information for Sacramento from wttr.in using curl and saves it as a PNG.
        Returns the path to the saved image.
        """
        try:
            # Create a timestamp for the filename
            timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            screenshot_filename = f"sacramento_weather_{timestamp}.png"
            screenshot_path = os.path.join(self.assets_dir, screenshot_filename) # save to the proper location

            # Use curl to get the weather data from wttr.in and save it as a PNG.
            # add the scale #2 to make the png larger
            curl_command = [
                "curl",
                "-s",  # Silent mode
                "v2.wttr.in/Sacramento.png?0pq&scale=.5",  # Fetch weather data for Sacramento
                "-o",
                screenshot_path,
            ]
            self.delete_old_screenshots()
            subprocess.run(curl_command, check=True)

            return screenshot_path

        except subprocess.CalledProcessError as e:
            print(f"Error fetching weather data: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None
