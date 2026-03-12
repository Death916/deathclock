#[derive(Debug, Clone)]
pub enum Sport {
    NBA,
    NFL,
    MLB,
}

#[derive(Debug)]
pub struct Game {
    pub sport: Sport,
    pub team1: String,
    pub team2: String,
    pub score1: String,
    pub score2: String,
    pub period: u8,
}

impl Game {
    pub fn new(
        sport: Sport,
        team1: &str,
        team2: &str,
        score1: &str,
        score2: &str,
        period: u8,
    ) -> Self {
        Game {
            sport,
            team1: team1.to_string(),
            team2: team2.to_string(),
            score1: score1.to_string(),
            score2: score2.to_string(),
            period,
        }
    }

    pub fn update(&mut self, score1: &str, score2: &str, period: u8) {
        self.score1 = score1.to_string();
        self.score2 = score2.to_string();
        self.period = period;
    }
}

pub fn sports() -> Vec<Game> {
    vec![
        Game::new(Sport::NBA, "Lakers", "Warriors", "100", "95", 3),
        Game::new(Sport::NBA, "Celtics", "Nets", "110", "105", 2),
        Game::new(Sport::MLB, "Red Sox", "Yankees", "100", "95", 1),
    ]
}

pub fn update_nba() -> Vec<Game> {
    let nba_games =
        ureq::get("https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json")
            .header("User-Agent", "deathclock-app/1.0")
            .call()
            .unwrap()
            .into_body()
            .read_to_vec()
            .unwrap();

    let json: serde_json::Value = serde_json::from_slice(&nba_games).unwrap();
    let games = json["scoreboard"]["games"].as_array().unwrap();
    let mut updated_games: Vec<Game> = Vec::new();

    for game in games {
        let game_id = game["gameId"].as_str().unwrap();
        let home_team = game["homeTeam"]["teamName"].as_str().unwrap();
        let away_team = game["awayTeam"]["teamName"].as_str().unwrap();
        let home_score = game["homeTeam"]["score"].as_u64().unwrap().to_string();
        let away_score = game["awayTeam"]["score"].as_u64().unwrap().to_string();
        let period = game["period"].as_u64().unwrap() as u8;

        let mut game = Game::new(
            Sport::NBA,
            home_team,
            away_team,
            &home_score,
            &away_score,
            period,
        );
        game.update(&home_score, &away_score, period);
        updated_games.push(game);
        println!("Game ID: {}", game_id);
        println!("Home Team: {}", home_team);
        println!("Away Team: {}", away_team);
        println!("Home Score: {}", home_score);
        println!("Away Score: {}", away_score);
        println!("Period: {}", period);
    }
    updated_games
}
