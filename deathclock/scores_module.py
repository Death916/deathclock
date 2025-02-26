from dash import html, Input, Output
from scores import NBAScores  # Import NBAScores class

class ScoresModule:
    def __init__(self, app):
        self.app = app
        self.scores_obj = self.get_scores_object()
        self.setup_callbacks()

    def get_scores_object(self):
        return NBAScores()

    def setup_callbacks(self):
        @self.app.callback(
            Output('nba-scores-display', 'children'),
            Input('nba-interval', 'n_intervals')
        )
        def update_scores(n):
            try:
                games = self.scores_obj.get_scores()
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
