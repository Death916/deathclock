from dash import Dash, html, dcc
from weather_module import WeatherModule
from news_module import NewsModule
from scores_module import ScoresModule
from alarm_module import AlarmModule
from clock_module import ClockModule

def create_app():
    app = Dash(__name__)
    
    app.layout = html.Div([
        html.H1(id='clock-display', style={'textAlign': 'center', 'cursor': 'pointer'}),
        dcc.Input(id='time-input', type='time', style={'display': 'none', 'margin': '0 auto'}),
        html.Div(id='output-selected-time', style={'textAlign': 'center', 'marginBottom': '20px'}),
        
        html.Div([
            html.Div([
                html.Div([
                    html.H2("NBA Scores"),
                    html.Div(id='nba-scores-display', className='score-container')
                ]),
                html.Div(id='weather-display')
            ], id='scores-weather-container'),
        ]),
        
        html.Div(id='news-ticker'),
        
        dcc.Interval(id='clock-interval', interval=60000, n_intervals=0),
        dcc.Interval(id='weather-interval', interval=150000, n_intervals=0),
        dcc.Interval(id='news-interval', interval=300000, n_intervals=0),
        dcc.Interval(id='nba-interval', interval=300000, n_intervals=0)
    ])
    
    ClockModule(app)
    WeatherModule(app)
    NewsModule(app)
    ScoresModule(app)
    alarm_module = AlarmModule(app)
    
    def check_alarms():
        trigg = alarm_module.alarm_obj.check_alarm()
        if trigg:
            print("ALARM TRIGGERED!")
    
    check_alarms()
    return app

if __name__ == '__main__':
    app = create_app()
    app.run_server(debug=False, host='0.0.0.0', port=8050)
