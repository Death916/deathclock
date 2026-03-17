use std::collections::HashMap;
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

pub fn update_mlb() -> Vec<Game> {
    let date = chrono::Local::now().format("%Y-%m-%d").to_string();
    let mlb_url = format!(
        "https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={}",
        date
    );
    let mlb_games = ureq::get(&mlb_url)
        .header("User-Agent", "deathclock-app/1.0")
        .call()
        .unwrap()
        .into_body()
        .read_to_vec()
        .unwrap();

    let mlb_json: serde_json::Value = serde_json::from_slice(&mlb_games).unwrap();
    let games = mlb_json["dates"][0]["games"].as_array().unwrap();

    let mut mlb_games_vec = Vec::new();

    for game in games {
        let home_team = game["teams"]["away"]["team"]["name"].as_str().unwrap();
        let away_team = game["teams"]["home"]["team"]["name"].as_str().unwrap();
        let home_score = game["teams"]["away"]["score"]
            .as_str()
            .unwrap_or_else(|| "0");
        let away_score = game["teams"]["home"]["score"]
            .as_str()
            .unwrap_or_else(|| "0");
        let period = game["status"]["period"]
            .as_str()
            .unwrap_or_default()
            .parse::<u8>()
            .unwrap_or_default();

        let mut mlb_game_struct = Game::new(
            Sport::MLB,
            home_team,
            away_team,
            home_score,
            away_score,
            period,
        );
        mlb_game_struct.update(&home_score, &away_score, period);
        mlb_games_vec.push(mlb_game_struct);
        println!("Home Team: {}", home_team);
        println!("Away Team: {}", away_team);
        println!("Home Score: {}", home_score);
        println!("Away Score: {}", away_score);
        println!("Period: {}", period);
    }

    mlb_games_vec
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

pub fn get_mlb_logos() -> HashMap<String, Vec<u8>> {
    let json = std::fs::read_to_string("src/files/mlb_logos.json").unwrap();
    let parsed_json: serde_json::Value = serde_json::from_str(&json).unwrap();
    let teams = parsed_json.as_array().unwrap();

    let mut logos_map = std::collections::HashMap::new();
    for team in teams {
        let team_name = team["name"].as_str().unwrap();
        let logo_url = team["logo"].as_str().unwrap();
        logos_map.insert(team_name.to_string(), logo_url.to_string());
    }
    let mut logos_svg_map = std::collections::HashMap::new();
    for (team_name, logo_url) in logos_map.iter() {
        let response = ureq::get(logo_url)
            .header("User-Agent", "deathclock-app/0.1")
            .call()
            .unwrap();

        let image_data = response.into_body().read_to_vec().unwrap();
        logos_svg_map.insert(team_name.to_string(), image_data);
    }
    logos_svg_map
}

pub fn get_nba_logos() -> HashMap<String, Vec<u8>> {
    let json = std::fs::read_to_string("src/files/nba_logos.json").unwrap();
    let parsed_json: serde_json::Value = serde_json::from_str(&json).unwrap();
    let teams = parsed_json.as_array().unwrap();

    let mut logos_map = std::collections::HashMap::new();
    for team in teams {
        let team_name = team["name"].as_str().unwrap();
        let logo_url = team["logo"].as_str().unwrap();
        logos_map.insert(team_name.to_string(), logo_url.to_string());
    }
    let mut nba_svg_map = std::collections::HashMap::new();
    for (team_name, logo_url) in logos_map.iter() {
        let response = ureq::get(logo_url)
            .header("User-Agent", "deathclock-app/0.1")
            .call()
            .unwrap();
        println!("Response {}", response.status());

        let image_data = response.into_body().read_to_vec().unwrap();
        nba_svg_map.insert(team_name.to_string(), image_data);
        println!("Downloaded logo for {}", team_name);
    }
    nba_svg_map
}
