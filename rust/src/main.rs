use iced::Application;
use iced::Center;
use iced::Element;
use iced::executor;
use iced::widget::{Column, button, column,PaneGrid, text};
use iced::window;

pub fn main() -> iced::Result {
    iced::run(Counter::update, Counter::view)
}

#[derive(Debug, Clone)]
enum Sport {
    NBA,
    NFL,
    MLB,
}

struct State {
    current_time: chrono::DateTime<chrono::Utc>,
    next_alarm: Option<chrono::DateTime<chrono::Utc>>,
    news: Vec<String>,
    weather: String,
    location: String,
    scores: Vec<Game>,
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
    
    fn update(&mut self, score1: &str, score2: &str) {
        self.score1 = score1.to_string();
        self.score2 = score2.to_string();
    }
    
    fn view(&self) -> Column<'_, Message> {
        let game = sports();
        let games = game.scores;

        column![
            text("scores").size(50),
            //text().size(20),
            text(format!("{} vs {}", games[0].team1, games[0].team2)).size(20),
            text(format!("{} - {}", games[0].score1, games[0].score2)).size(20),
        ]
        .padding(20)
        .align_x(Center)
    }
}
fn sports() -> State {
    println!("Sports!");

    let mut state = State {
        current_time: chrono::Utc::now(),
        next_alarm: Some(chrono::Utc::now() + chrono::Duration::hours(1)),
        news: vec!["Breaking news!".to_string()],
        weather: "Sunny".to_string(),
        location: "Sacramento".to_string(),
        scores: Vec::new(),
    };

    state
        .scores
        .push(Game::new(Sport::NBA, "Lakers", "Warriors", "100", "95"));
    state
        .scores
        .push(Game::new(Sport::NBA, "Celtics", "Nets", "110", "105"));
    state
        .scores
        .push(Game::new(Sport::MLB, "Red Sox", "Yankees", "100", "95"));
    println!("{:?}", state.current_time);
    println!("---------------");

    for game in &state.scores {
        println!("+----------------------+");
        println!("| Sport: {:?}", game.sport);
        println!("| {} vs {}", game.team1, game.team2);
        println!("| {} - {}", game.score1, game.score2);
        println!("+----------------------+");
    }
    state
}

#[derive(Default)]
struct Counter {
    value: i64,
}

#[derive(Debug, Clone, Copy)]
enum Message {
    Increment,
    Decrement,
}

impl Counter {
    fn update(&mut self, message: Message) {
        match message {
            Message::Increment => {
                self.value += 1;
            }
            Message::Decrement => {
                self.value -= 1;
            }
        }
    }

    fn view(&self) -> Column<'_, Message> {
        let game = sports();
        let games = game.scores;

        column![
            text(self.value).size(50),
            //text().size(20),
            text(format!("{} vs {}", games[0].team1, games[0].team2)).size(20),
            text(format!("{} - {}", games[0].score1, games[0].score2)).size(20),
        ]
        .padding(20)
        .align_x(Center)
    }
}
