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


app.layout = html.Div([
    html.H1(id='clock-display', style={'textAlign': 'center'}),
    html.Div(id='weather-display', style={'textAlign': 'center'}),
    html.Div(id='news-ticker', className='ticker'),
    dcc.Interval(id='clock-interval', interval=1000, n_intervals=0),
    dcc.Interval(id='weather-interval', interval=300000, n_intervals=0),
    dcc.Interval(id='news-interval', interval=300000, n_intervals=0),
    
    html.Div([
        html.H2("NBA Scores"),
        html.Div(id='nba-scores-display', className='score-container'),
        dcc.Interval(id='nba-interval', interval=60000, n_intervals=0)
    ])
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
    try:
        news_dict = news_obj.get_news()
        items = [html.Span(f"{headline} | ", className='news-item') 
                for headline in news_dict.keys()]
        return html.Div(items)
    except Exception as e:
        return html.Div(f"News feed error: {str(e)}")

 #get the scores from the scores API   
@app.callback(
    Output('nba-scores-display', 'children'),
    Input('nba-interval', 'n_intervals')
)
def update_scores(n):
    try:
        games = scores_obj.get_scores()
        return [
            html.Div([
                html.Div([
                    html.Span(f"{game['away_team']} {game['away_score']}"),
                    html.Span(" @ "),
                    html.Span(f"{game['home_team']} {game['home_score']}")
                ], className='game-score'),
                html.Div(f"Period: {game['period']}", className='game-period')
            ], className='score-box') 
            for game in games
        ]
    except Exception as e:
        return html.Div("Scores unavailable")

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
