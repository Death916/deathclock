use iced::Center;
use iced::widget::{Column, PaneGrid, button, column, text, image,row,Row,};
use iced::Element;
pub fn main() -> iced::Result {
    iced::application(State::default, State::update, State::view).run()
}

#[derive(Debug, Clone)]
enum Sport {
    NBA,
    NFL,
    MLB,
}

#[derive(Debug)]
struct State {
    current_time: chrono::DateTime<chrono::Utc>,
    next_alarm: Option<chrono::DateTime<chrono::Utc>>,
    news: Vec<String>,
    weather: Vec<u8>,
    location: String,
    scores: Vec<Game>,
}
impl State {
    fn update(&mut self, scores: Vec<Game>) {
        self.scores = scores;    
        
    }

    fn view(&self) -> Element<'_, Vec<Game>> {
        let game = sports();
        let games = game.scores;
        let weather_img = image::Handle::from_bytes(self.weather.clone());
        column![
            text("scores").size(50),
            //text().size(20),
            text(format!("{} vs {}", games[0].team1, games[0].team2)).size(20),
            text(format!("{} - {}", games[0].score1, games[0].score2)).size(20),
            
            row![
                text("Weather").size(20),
                image(weather_img).width(50),
                text(self.location.clone()).size(20),
            ]
        ]
        .padding(20)
        .align_x(Center)
        .into()
    }
}    

impl Default for State {
    fn default() -> Self {
        let text = ureq::get("https://github.com/iced-rs/iced/blob/9712b319bb7a32848001b96bd84977430f14b623/examples/resources/ferris.png?raw=true")
            .call().unwrap()
            .body_mut()
            .read_to_vec().unwrap();

        State {
            current_time: chrono::Utc::now(),
            next_alarm: None,
            news: Vec::new(),
            weather: text,
            location: "Sacramento".to_string(),
            scores: Vec::new(),
        }
    }
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
}

fn sports() -> State {
    println!("Sports!");
    let mut state = State {
        current_time: chrono::Utc::now(),
        next_alarm: Some(chrono::Utc::now() + chrono::Duration::hours(1)),
        news: vec!["Breaking news!".to_string()],
        weather: Vec::new(),
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
