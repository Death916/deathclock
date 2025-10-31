# /home/death916/code/python/deathclock/utils/scores.py
from nba_api.live.nba.endpoints import scoreboard
from datetime import datetime, timedelta
import statsapi
import reflex as rx
import logging  # Use logging for consistency


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class NBAScores(rx.Base):
    async def get_scores(self):  # Make async to match usage in State
        """Fetches NBA scores and returns them as a list of dicts."""
        try:
            # Get scoreboard data

            board = scoreboard.ScoreBoard()
            data = board.get_dict()

            # Check if we have a valid scoreboard response
            if "scoreboard" not in data:
                logging.warning("No NBA scoreboard data found in response")
                return []

            games = data["scoreboard"].get("games", [])
            if not games:
                logging.info("No active NBA games found in scoreboard")
                return []

            scores_list = []
            for game in games:
                try:
                    game_data = {
                        "home_team": game["homeTeam"]["teamTricode"],
                        "home_score": game["homeTeam"]["score"],
                        "away_team": game["awayTeam"]["teamTricode"],
                        "away_score": game["awayTeam"]["score"],
                        "period": game["period"],
                        "status": game["gameStatusText"],
                    }
                    scores_list.append(game_data)
                except KeyError as e:
                    logging.error(
                        f"Error processing NBA game data: {e} for game: {game.get('gameId', 'N/A')}"
                    )
                    continue  # Skip this game

            return scores_list

        except Exception as e:
            logging.error(f"Error fetching NBA scores: {e}", exc_info=True)
            return []  # Return empty list on error


class mlbScores(rx.Base):
    async def get_games(self):  # Make async
        """Fetches MLB games data."""
        try:
            games = statsapi.schedule()  # Assuming sync for now
            return games
        except Exception as e:
            logging.error(f"Error fetching MLB games: {e}", exc_info=True)
            return []

    async def get_scores(self):  # Make async to match usage in State
        """Fetches and formats MLB scores."""
        games = await self.get_games()  # Await the async get_games
        scores_list = []
        if not games:
            logging.info("No MLB games found today.")
            return []
        for game in games:
            try:
                # Ensure keys exist, provide defaults if necessary
                game_data = {
                    "home_team": game.get("home_name", "N/A"),
                    "home_score": game.get("home_score", "-"),
                    "away_team": game.get("away_name", "N/A"),
                    "away_score": game.get("away_score", "-"),
                    "status": game.get("status", "Scheduled"),  # Provide default status
                }
                scores_list.append(game_data)
            except KeyError as e:
                # This block might be less necessary with .get() above
                logging.error(
                    f"Error processing MLB game data: {e} for game: {game.get('game_id', 'N/A')}"
                )
                continue  # Skip this game
        return scores_list  # RETURN THE LIST


class nflScores:
    async def get_scores(self):
        # get nfl scores from espn
        nfl_scores = []
        try:
            import aiohttp

            # use current local date in YYYYMMDD format
            date_str = datetime.now().strftime("%Y%m%d")
            url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?dates={date_str}"

            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=15) as resp:
                    if resp.status != 200:
                        logging.error(
                            f"ESPN NFL scoreboard returned status {resp.status}"
                        )
                        return []
                    data = await resp.json()

            events = data.get("events", [])
            if not events:
                logging.info("No NFL games found for date %s", date_str)
                return []

            nfl_scores = []
            for ev in events:
                try:
                    competitions = ev.get("competitions", [])
                    if not competitions:
                        logging.warning(
                            "No competitions found for event: %s", ev.get("id")
                        )
                        continue
                    comp = competitions[0]
                    competitors = comp.get("competitors", [])
                    home_team = away_team = "N/A"
                    home_score = away_score = "-"

                    for c in competitors:
                        team = c.get("team", {}) or {}
                        abbr = (
                            team.get("abbreviation")
                            or team.get("displayName")
                            or team.get("shortDisplayName")
                            or "N/A"
                        )
                        score = (
                            c.get("score", "-") if c.get("score") is not None else "-"
                        )
                        homeAway = c.get("homeAway", "").lower()
                        if homeAway == "home":
                            home_team = abbr
                            home_score = score
                        else:
                            away_team = abbr
                            away_score = score

                    status = comp.get("status", {}) or {}
                    status_type = status.get("type", {}) or {}
                    status_text = (
                        status_type.get("shortDetail")
                        or status_type.get("description")
                        or status_type.get("state")
                        or status.get("type")
                        or status.get("detail")
                        or "Unknown"
                    )

                    game_data = {
                        "home_team": home_team,
                        "home_score": home_score,
                        "away_team": away_team,
                        "away_score": away_score,
                        "status": status_text,
                    }
                    nfl_scores.append(game_data)
                except Exception as e:
                    logging.error(
                        f"Error processing NFL event: {e} for event {ev.get('id')}",
                        exc_info=True,
                    )
                    continue
            print(nfl_scores)
            return nfl_scores

        except Exception as e:
            logging.error(f"Error fetching NFL scores: {e}", exc_info=True)
            return []


if __name__ == "__main__":
    import asyncio

    async def test_scores():
        nba_client = NBAScores()
        nba_results = await nba_client.get_scores()  # await async method

        print("\nNBA Scores:")
        if nba_results:
            for game in nba_results:
                print(
                    f"{game['away_team']} {game['away_score']} @ "
                    f"{game['home_team']} {game['home_score']}  "
                    f"(Status: {game['status']})"
                )
        else:
            print("No NBA games/scores available")

        mlb_client = mlbScores()
        mlb_results = await mlb_client.get_scores()  # await async method

        print("\nMLB Scores:")
        if mlb_results:
            for game in mlb_results:
                print(
                    f"{game['away_team']} {game['away_score']} @ "
                    f"{game['home_team']} {game['home_score']}  "
                    f"(Status: {game['status']})"
                )
        else:
            print("No MLB games/scores available")

        nfl_client = nflScores()
        nfl_results = await nfl_client.get_scores()  # await async method

        print("\nNFL Scores:")
        if nfl_results:
            for game in nfl_results:
                print(
                    f"{game['away_team']} {game['away_score']} @ "
                    f"{game['home_team']} {game['home_score']}  "
                    f"(Status: {game['status']})"
                )
        else:
            print("No NFL games/scores available")

    asyncio.run(test_scores())
