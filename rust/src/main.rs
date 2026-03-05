fn main() {
    #[derive(Debug)]
    enum Sport {
        NBA,
        NFL,
        MLB,
    }

    #[derive(Debug)]
    struct Game {
        sport: Sport,
        team1: String,
        team2: String,
        score1: String,
        score2: String,
    }

    impl Game {
        fn new(sport: Sport, team1: &str, team2: &str, score1: &str, score2: &str) -> Self {
            Game {
                sport,
                team1: team1.to_string(),
                team2: team2.to_string(),
                score1: score1.to_string(),
                score2: score2.to_string(),
            }
        }
    }

    struct State {
        current_time: chrono::DateTime<chrono::Utc>,
        next_alarm: Option<chrono::DateTime<chrono::Utc>>,
        news: Vec<String>,
        weather: String,
        location: String,
        scores: Vec<Game>,
    }

    let mut state = State {
        current_time: chrono::Utc::now(),
        next_alarm: Some(chrono::Utc::now() + chrono::Duration::hours(1)),
        news: vec!["Breaking news!".to_string()],
        weather: "Sunny".to_string(),
        location: "Sacramento".to_string(),
        scores: Vec::new(),
    };

    state.scores.push(Game::new(Sport::NBA, "Lakers", "Warriors", "100", "95"));
    state.scores.push(Game::new(Sport::NBA, "Celtics", "Nets", "110", "105"));
    state.scores.push(Game::new(Sport::MLB, "Red Sox", "Yankees", "100", "95"));

    println!("{:?}", state.current_time);
    println!("---------------");

    for game in &state.scores {
        println!("+----------------------+");
        println!("| Sport: {:?}", game.sport);
        println!("| {} vs {}", game.team1, game.team2);
        println!("| {} - {}", game.score1, game.score2);
        println!("+----------------------+");
    }
}
