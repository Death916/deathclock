#[derive(Debug)]
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
}

impl Game {
    pub fn new(sport: Sport, team1: &str, team2: &str, score1: &str, score2: &str) -> Self {
        Game {
            sport,
            team1: team1.to_string(),
            team2: team2.to_string(),
            score1: score1.to_string(),
            score2: score2.to_string(),
        }
    }
}

pub fn sample_scores() -> Vec<Game> {
    vec![
        Game::new(Sport::NBA, "Lakers", "Warriors", "100", "95"),
        Game::new(Sport::NBA, "Celtics", "Nets", "110", "105"),
        Game::new(Sport::MLB, "Red Sox", "Yankees", "100", "95"),
    ]
}
