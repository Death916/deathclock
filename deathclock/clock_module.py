from time import strftime, localtime
from dash import Input, Output

class ClockModule:
    def __init__(self, app):
        self.app = app
        self.setup_callbacks()

    def setup_callbacks(self):
        @self.app.callback(
            Output('clock-display', 'children'),
            Input('clock-interval', 'n_intervals')
        )
        def update_time(n):
            return strftime("%B %d, %I:%M %p", localtime())
