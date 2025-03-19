import datetime
import os
from dash import html, Input, Output
from weather import Weather  # Import Weather class

class WeatherModule:
    def __init__(self, app):
        self.app = app
        self.weather_obj = self.get_weather_object()
        self.setup_callbacks()

    def get_weather_object(self):
        return Weather()

    def setup_callbacks(self):
        @self.app.callback(
            Output('weather-display', 'children'),
            Input('weather-interval', 'n_intervals')
        )
        def update_weather(n):
            try:
                print("UPDATING WEATHER...")
                screenshot_path = self.weather_obj.get_weather_screenshot()
                image_name = os.path.basename(screenshot_path)
                return html.Div(
                    [
                        html.H2("Sacramento Weather"),
                        html.Img(
                            src=self.app.get_asset_url(image_name + f"?v={datetime.datetime.now().timestamp()}"),
                            style={"width": "100%", "display": "block", "image-rendering": "crisp-edges"}
                        ),
                    ],
                    style={"width": "600px", "margin": "0 auto", "border": "1px solid black"}
                )
            except Exception as e:
                return html.Div(f"Weather update error: {str(e)}")
