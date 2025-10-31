# /home/death916/code/python/deathclock/utils/scores.py
from nba_api.live.nba.endpoints import scoreboard
from datetime import datetime, timedelta
import statsapi
import reflex as rx
import logging # Use logging for consistency

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NBAScores(rx.Base):

    async def get_scores(self): # Make async to match usage in State
        """Fetches NBA scores and returns them as a list of dicts."""
        try:
            # Get scoreboard data
            # Consider running blocking IO in a thread pool if it becomes an issue
            board = scoreboard.ScoreBoard()
            data = board.get_dict()

            # Check if we have a valid scoreboard response
            if 'scoreboard' not in data:
                logging.warning("No NBA scoreboard data found in response")
                return []

            games = data['scoreboard'].get('games', [])
            if not games:
                logging.info("No active NBA games found in scoreboard")
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
                    logging.error(f"Error processing NBA game data: {e} for game: {game.get('gameId', 'N/A')}")
                    continue # Skip this game

            # No need to store in self._scores if this is just a utility
            return scores_list

        except Exception as e:
            logging.error(f"Error fetching NBA scores: {e}", exc_info=True)
            return [] # Return empty list on error

class mlbScores(rx.Base):

    async def get_games(self): # Make async
        """Fetches MLB games data."""
        try:
            games = statsapi.schedule() # Assuming sync for now
            return games
        except Exception as e:
            logging.error(f"Error fetching MLB games: {e}", exc_info=True)
            return []

    async def get_scores(self): # Make async to match usage in State
        """Fetches and formats MLB scores."""
        games = await self.get_games() # Await the async get_games
        scores_list = []
        if not games:
             logging.info("No MLB games found today.")
             return []
        for game in games:
            try:
                # Ensure keys exist, provide defaults if necessary
                game_data = {
                    'home_team': game.get('home_name', 'N/A'),
                    'home_score': game.get('home_score', '-'),
                    'away_team': game.get('away_name', 'N/A'),
                    'away_score': game.get('away_score', '-'),
                    'status': game.get('status', 'Scheduled') # Provide default status
                }
                scores_list.append(game_data)
            except KeyError as e:
                # This block might be less necessary with .get() above
                logging.error(f"Error processing MLB game data: {e} for game: {game.get('game_id', 'N/A')}")
                continue # Skip this game
        return scores_list # RETURN THE LIST

# Keep the __main__ block for testing if desired, but update calls to be async if needed
if __name__ == "__main__":
    import asyncio

    async def test_scores():
        nba_client = NBAScores()
        nba_results = await nba_client.get_scores() # await async method

        print("\nNBA Scores:")
        if nba_results:
            for game in nba_results:
                print(f"{game['away_team']} {game['away_score']} @ "
                      f"{game['home_team']} {game['home_score']}  "
                      f"(Status: {game['status']})")
        else:
            print("No NBA games/scores available")

        mlb_client = mlbScores()
        mlb_results = await mlb_client.get_scores() # await async method

        print("\nMLB Scores:")
        if mlb_results:
            for game in mlb_results:
                 print(f"{game['away_team']} {game['away_score']} @ "
                       f"{game['home_team']} {game['home_score']}  "
                       f"(Status: {game['status']})")
        else:
            print("No MLB games/scores available")

    asyncio.run(test_scores())
