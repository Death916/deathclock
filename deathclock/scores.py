from nba_api.live.nba.endpoints import scoreboard
from datetime import datetime, timedelta

class NBAScores:
    def __init__(self):
        self._scores = []
        
    def get_scores(self):
        try:
            # Get scoreboard data
            board = scoreboard.ScoreBoard()
            data = board.get_dict()
            
            # Check if we have a valid scoreboard response
            if 'scoreboard' not in data:
                print("No scoreboard data found")
                return []
                
            games = data['scoreboard'].get('games', [])
            if not games:
                print("No games found in scoreboard")
                return []
            
            scores_list = []
            for game in games:
                try:
                    game_data = {
                        'home_team': game['homeTeam']['teamTricode'],
                        'home_score': game['homeTeam']['score'],
                        'away_team': game['awayTeam']['teamTricode'],
                        'away_score': game['awayTeam']['score'],
                        'period': game['period'],
                        'status': game['gameStatusText']
                    }
                    scores_list.append(game_data)
                except KeyError as e:
                    print(f"Error processing game data: {e}")
                    continue
            
            self._scores = scores_list
            return self._scores
            
        except Exception as e:
            print(f"Error fetching scores: {e}")
            return []

if __name__ == "__main__":
    scores = NBAScores()
    results = scores.get_scores()
    
    print("\nNBA Scores:")
    if results:
        for game in results:
            print(f"{game['away_team']} {game['away_score']} @ "
                  f"{game['home_team']} {game['home_score']}  "
                  f"(Status: {game['status']})")
    else:
        print("No games available")
