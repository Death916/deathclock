from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import datetime
from time import strftime, localtime
from weather import Weather
from news import News
from scores import NBAScores
app = Dash(__name__)

# Initialize classes
weather_obj = Weather()
news_obj = News()
scores_obj = NBAScores()
#uses arbitrary date in the past as initial value
_last_news_update = datetime.datetime(2000, 1, 1)
_cached_news = []
_initial_run = True
_timer_elapsed = False
app.layout = html.Div([
    html.H1(id='clock-display', style={'textAlign': 'center'}),
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
    html.Div(id='news-ticker', className='ticker'),
    # Intervals
    dcc.Interval(id='clock-interval', interval=1000, n_intervals=0),
    dcc.Interval(id='weather-interval', interval=300000, n_intervals=0),
    dcc.Interval(id='news-interval', interval=300000, n_intervals=0),
    dcc.Interval(id='nba-interval', interval=60000, n_intervals=0)
])



    

@app.callback(
    Output('clock-display', 'children'),
    Input('clock-interval', 'n_intervals')
)
def update_time(n):
    return strftime("%B %d, %I:%M %p", localtime())

@app.callback(
    Output('weather-display', 'children'),
    Input('weather-interval', 'n_intervals')
)
def update_weather(n):
    try:
        weather_obj.get_weather_screenshot()
        return html.Div([
            html.H2("Sacramento Weather"),
            html.Img(src=app.get_asset_url('sacramento_weather_map.png'),
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
    # On first run or if 5 minutes have elapsed since last update
    if _initial_run or (current_time - _last_news_update).total_seconds() >= 300:
        print("Fetching fresh news...")
        try:
            headlines_dict = news_obj.get_news()
            if not isinstance(headlines_dict, dict):
                return html.Div("News update error: Invalid data format")
            if not headlines_dict:
                return html.Div("No news fetched")

            combined_text = " | ".join(headlines_dict.keys())
            text_px = len(combined_text) * 8  # Approx 8px per character
            scroll_speed = 500  # px per second
            duration = text_px / scroll_speed  # seconds to scroll across

            # Enforce a floor duration so it's not too quick for short text
            if duration < 20:
                duration = 20

            ticker_style = {"animationDuration": f"{duration}s", "whiteSpace": "nowrap"}
            
            items = [
                html.Div(
                    f"{headline} | ",
                    className="news-item",
                    style=ticker_style
                )
                for headline in headlines_dict.keys()
            ]

            _cached_news = html.Div(items, style=ticker_style)
            _last_news_update = current_time
            _initial_run = False
            return _cached_news

        except Exception as e:
            return html.Div(f"News feed error: {str(e)}")

    print("Returning cached news...")
    return _cached_news



   

 #get the scores from the scores API   
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

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
