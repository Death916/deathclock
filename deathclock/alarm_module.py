import datetime
from dash import html, dcc, Input, Output, State
import alarm # Import Alarm class

class AlarmModule:
    def __init__(self, app):
        self.app = app
        self.alarm_obj = self.get_alarm_object()
        self._alarm_time = None
        self.setup_callbacks()

    def get_alarm_object(self):
        return alarm.Alarm()

    def setup_callbacks(self):
        @self.app.callback(
            Output('time-input', 'style'),
            Input('clock-display', 'n_clicks'),
            State('time-input', 'style')
        )
        def toggle_time_input(n_clicks, current_style):
            if n_clicks and n_clicks % 2 == 1:
                return {'display': 'block', 'margin': '0 auto'}
            return {'display': 'none', 'margin': '0 auto'}

        @self.app.callback(
            Output('output-selected-time', 'children'),
            Input('time-input', 'value')
        )
        def process_selected_time(time_value):
            if time_value:
                self._alarm_time = time_value
                self.alarm_obj.add_alarm(time_value, datetime.datetime.now())
                return f'Alarm time: {time_value}'
            return 'No time selected yet.'
