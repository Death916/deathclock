from dash import Dash, html, dcc, Input, Output, State
import datetime
from time import strftime, localtime
from weather import Weather
from news import News
from scores import NBAScores
import alarm

app = Dash(__name__)

# Initialize classes
weather_obj = Weather()
news_obj = News()
scores_obj = NBAScores()
alarm_obj = alarm.Alarm()
_alarm_time = None

# Uses arbitrary date in the past as initial value
_last_news_update = datetime.datetime(2000, 1, 1)
_cached_news = []
_initial_run = True
_timer_elapsed = False

# Layout includes:
# - The clock display (clickable) as an H1 element
# - A hidden time input that will appear on clicking the clock
# - An output div for the selected time
app.layout = html.Div([
    html.H1(id='clock-display', style={'textAlign': 'center', 'cursor': 'pointer'}),
    dcc.Input(id='time-input', type='time', style={'display': 'none', 'margin': '0 auto'}),
    html.Div(id='output-selected-time', style={'textAlign': 'center', 'marginBottom': '20px'}),
    
    html.Div([
        # Container for scores and weather
        html.Div([
            html.Div([
                html.H2("NBA Scores"),
                html.Div(id='nba-scores-display', className='score-container')
            ]),
            html.Div(id='weather-display')
        ], id='scores-weather-container'),
    ]),
    #add class back if not working still
    html.Div(id='news-ticker'),
    # Intervals
    dcc.Interval(id='clock-interval', interval=60000, n_intervals=0),
    dcc.Interval(id='weather-interval', interval=150000, n_intervals=0),
    dcc.Interval(id='news-interval', interval=300000, n_intervals=0),
    dcc.Interval(id='nba-interval', interval=300000, n_intervals=0)
])


@app.callback(
    Output('clock-display', 'children'),
    Input('clock-interval', 'n_intervals')
)
def update_time(n):
    return strftime("%B %d, %I:%M %p", localtime())


# When the clock display is clicked, show the time input.
@app.callback(
    Output('time-input', 'style'),
    Input('clock-display', 'n_clicks'),
    State('time-input', 'style')
)
def toggle_time_input(n_clicks, current_style):
    if n_clicks and n_clicks % 2 == 1:
        # On odd clicks, display the time input.
        return {'display': 'block', 'margin': '0 auto'}
    return {'display': 'none', 'margin': '0 auto'}


# Callback to process the selected time from the time input.
@app.callback(
    Output('output-selected-time', 'children'),
    Input('time-input', 'value')
)
def process_selected_time(time_value):
    if time_value:
        # Here you can pass time_value to another function if desired.
        global alarm_time
        alarm_time = time_value
        alarm_obj.add_alarm(time_value, datetime.datetime.now())
        return f'Alarm time: {time_value}'
    return 'No time selected yet.'


@app.callback(
    Output('weather-display', 'children'),
    Input('weather-interval', 'n_intervals')
)
def update_weather(n):
    try:
        print("UPDATING WEATHER...")
        weather_obj.get_weather_screenshot()
        return html.Div([
            html.H2("Sacramento Weather"),
            html.Img(src=app.get_asset_url('sacramento_weather_map.png'
                                            + f"?v={datetime.datetime.now().timestamp()}"),
                     style={'maxWidth': '500px'})
        ])
    except Exception as e:
        return html.Div(f"Weather update error: {str(e)}")


@app.callback(
    Output('news-ticker', 'children'),
    Input('news-interval', 'n_intervals')
)
def update_news(n):
    global _last_news_update, _cached_news, _initial_run
    current_time = datetime.datetime.now()
    try:
        print("UPDATING NEWS...")
        headlines_dict = news_obj.get_news()
        # Combine source and headline for each news item
        combined_items = " | ".join([f"{data['source']}: {headline}" 
                                   for headline, data in headlines_dict.items()])
        
        text_px = len(combined_items) * 8
        scroll_speed = 75
        duration = max(text_px / scroll_speed, 20)
        
        ticker_style = {"animationDuration": f"{duration}s"}
        
        _cached_news = html.Div(
            html.Span(combined_items, className="news-item", style=ticker_style),
            className='ticker'
        )
        _last_news_update = current_time
        _initial_run = False
        return _cached_news
        
    except Exception as e:
        if _cached_news:
            return _cached_news
        return html.Div("No news available.")


@app.callback(
    Output('nba-scores-display', 'children'),
    Input('nba-interval', 'n_intervals')
)
def update_scores(n):
    try:
        games = scores_obj.get_scores()
        if not games:
            return html.Div("No games available", className='text-center')
        return html.Div([
            html.Div([
                html.Div([
                    html.Span(f"{game['away_team']} {game['away_score']}"),
                    html.Span(" @ "),
                    html.Span(f"{game['home_team']} {game['home_score']}")
                ], className='game-score'),
                html.Div(f"Period: {game['period']}", className='game-period')
            ], className='score-box')
            for game in games
        ], className='score-container')
    except Exception as e:
        return html.Div("Scores unavailable")

# Check for alarms and play sound if triggered
def check_alarms():
    trigg = alarm_obj.check_alarm()
    if trigg:
        print("ALARM TRIGGERED!")
        # Play alarm sound here using dash audio component
check_alarms()



if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=8050)
