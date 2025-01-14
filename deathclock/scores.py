from nba_api.live.nba.endpoints import scoreboard
from nba_api.stats.endpoints import ScoreboardV2
from datetime import datetime, timedelta

class NBAScores:
    """
    A class to fetch NBA games/scores. It first attempts to fetch live games.
    If no live games are found, it falls back to historical data using ScoreboardV2.
    """
    def __init__(self):
        self._scores = []

    def get_scores(self):
        """
        Fetches today's NBA games. Falls back to yesterday's games if none are found.
        """
        try:
            # Try fetching live games
            board = scoreboard.ScoreBoard()
            live_games = board.get_dict().get('games', [])
            
            if live_games:
                self._scores = self._build_live_scores(live_games)
                return self._scores
            
            # If no live games, fetch yesterday's historical data
            yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            print("No live games found. Fetching yesterday's scores...")
            return self._get_historical_scores(yesterday)
        
        except Exception as e:
            print(f"Error fetching scores: {e}")
            return []

    def _build_live_scores(self, games):
        """
        Builds a list of game dictionaries from live game data.
        """
        scores_list = []
        for game in games:
            game_data = {
                'home_team': game['homeTeam']['teamTricode'],
                'home_score': game['homeTeam']['score'],
                'away_team': game['awayTeam']['teamTricode'],
                'away_score': game['awayTeam']['score'],
                'period': game['period'],
                'status': game['gameStatus']
            }
            scores_list.append(game_data)
        return scores_list

    def _get_historical_scores(self, date):
        """
        Fetches historical NBA scores for a specific date using ScoreboardV2.
        """
        try:
            board = ScoreboardV2(game_date=date)
            result_sets = board.get_dict().get('resultSets', [])
            
            # Check if resultSets contains at least one set
            if not result_sets or len(result_sets[0]['rowSet']) == 0:
                print(f"No historical data available for {date}.")
                return []
            
            games = result_sets[0]['rowSet']
            
            scores_list = []
            for game in games:
                game_data = {
                    'home_team': game[6],  # Home team abbreviation
                    'home_score': game[21],  # Home team score
                    'away_team': game[7],  # Away team abbreviation
                    'away_score': game[22],  # Away team score
                    'status': "Final"
                }
                scores_list.append(game_data)
            
            self._scores = scores_list
            return self._scores
        
        except Exception as e:
            print(f"Error fetching historical scores: {e}")
            return []

if __name__ == "__main__":
    """
    Run standalone to print out today's (or yesterday's) games.
    """
    nba_scores = NBAScores()
    results = nba_scores.get_scores()
    
    if not results:
        print("No NBA games found for today or yesterday.")
    else:
        for game in results:
            print(f"{game['away_team']} {game['away_score']} "
                  f"@ {game['home_team']} {game['home_score']}  "
                  f"(Status: {game['status']})")
