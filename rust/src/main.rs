use iced;

fn main() {
    struct State {
        current_time: chrono::DateTime<chrono::Utc>,
        next_alarm: Option<chrono::DateTime<chrono::Utc>>,
        news: Vec<String>,
        weather: String,
        location: String,
        scores: Vec<Scores>,
    }

    #[derive(Debug)]
    enum League {
        NBA(NbaScores),
        NFL(Vec<String>),
        MLB(Vec<String>),
    }

    #[derive(Debug)]
    struct Scores {
        nba: League,
        nfl: League,
        mlb: League,
    }

    #[derive(Debug)]
    struct NbaScores {
        teams: Vec<String>,
        team1: String,
        team2: String,
        score1: String,
        score2: String,
    }

    impl Scores {
        fn new() -> Self {
            Scores {
                nba: League::NBA(NbaScores {
                    teams: Vec::new(),
                    team1: String::new(),
                    team2: String::new(),
                    score1: String::new(),
                    score2: String::new(),
                }),
                nfl: League::NFL(Vec::new()),
                mlb: League::MLB(Vec::new()),
            }
        }
    }

    let mut scores = Scores::new();

    let state = State {
        current_time: chrono::Utc::now(),
        next_alarm: None,
        news: Vec::new(),
        weather: String::new(),
        location: String::new(),
        scores: Vec::new(),
    };

    let mut state = state;

    state.current_time = chrono::Utc::now();

    state.next_alarm = Some(chrono::Utc::now() + chrono::Duration::hours(1));

    state.news.push("Breaking news!".to_string());

    state.weather = "Sunny".to_string();

    state.location = "Sacramento".to_string();

    scores.nba = League::NBA(NbaScores {
        teams: vec![
            "Team A vs Team B".to_string(),
            "Team C vs Team D".to_string(),
        ],
        team1: "Team A".to_string(),
        team2: "Team B".to_string(),
        score1: "100".to_string(),
        score2: "95".to_string(),
    });
    state.scores.push(scores);

    
    println!("{:?}", state.current_time);
    println!("{:?}", state.scores);
    println!("{:?}", state.scores[0].nba);
    
    
}
