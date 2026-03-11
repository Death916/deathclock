use iced::Center;
use iced::Element;
use iced::widget::{column, image, pane_grid, row, text};
pub fn main() -> iced::Result {
    iced::run(State::update, State::view)
}

#[derive(Debug, Clone)]
enum Sport {
    NBA,
    NFL,
    MLB,
}

#[derive(Debug, Clone)]
enum Pane {
    Main,
    MlbPane,
    NflPane,
    NbaPane,
    Weather,
}

#[derive(Debug, Clone)]
enum Message {
    PaneDragged(pane_grid::DragEvent),
    PaneResized(pane_grid::ResizeEvent),
}

#[derive(Debug)]
struct State {
    current_time: chrono::DateTime<chrono::Utc>,
    next_alarm: Option<chrono::DateTime<chrono::Utc>>,
    news: Vec<String>,
    weather: Vec<u8>,
    location: String,
    scores: Vec<Game>,
    panes: pane_grid::State<Pane>,
}
impl State {
    fn update(&mut self, message: Message) {
        match message {
            Message::PaneDragged(pane_grid::DragEvent::Dropped { pane, target }) => {
                self.panes.drop(pane, target);
            }
            Message::PaneDragged(_) => {}
            Message::PaneResized(pane_grid::ResizeEvent { split, ratio }) => {
                self.panes.resize(split, ratio);
            }
        }
    }

    fn view(state: &State) -> Element<'_, Message> {
        pane_grid(&state.panes, |_pane, pane_state, _is_maximized| {
            let content: Element<'_, Message> = match pane_state {
                Pane::NbaPane => {
                    let games = &state.scores;
                    column![
                        text("NBA").size(50),
                        text(format!("{} vs {}", games[0].team1, games[0].team2)).size(20),
                        text(format!("{} - {}", games[0].score1, games[0].score2)).size(20),
                    ]
                    .padding(5)
                    .into()
                }
                Pane::NflPane => text("NFL").into(),
                Pane::MlbPane => text("MLB").into(),
                Pane::Main => text("Main").into(),
                Pane::Weather => {
                    let weather_img = image::Handle::from_bytes(state.weather.clone());
                    column![
                        text("Weather").size(50),
                        image(weather_img).width(100).height(100),
                        text(state.location.clone()).size(30),
                    ]
                    .padding(20)
                    .into()
                }
            };
            pane_grid::Content::new(content)
        })
        .on_drag(Message::PaneDragged)
        .on_resize(10, Message::PaneResized)
        .into()
    }
}

impl Default for State {
    fn default() -> Self {
        let text = ureq::get("https://v2.wttr.in/Sacramento.png?u0")
            .header("User-Agent", "deathclock-app/1.0")
            .call()
            .unwrap()
            .into_body()
            .read_to_vec()
            .unwrap();

        State {
            current_time: chrono::Utc::now(),
            next_alarm: None,
            news: Vec::new(),
            weather: text,
            location: "Sacramento".to_string(),
            scores: {
                sports_updates::update_nba();
                sports()
            },
            panes: {
                let (mut panes, nba) = pane_grid::State::new(Pane::NbaPane);
                let (weather, _) = panes
                    .split(pane_grid::Axis::Vertical, nba, Pane::Weather)
                    .unwrap();
                let (nfl, _) = panes
                    .split(pane_grid::Axis::Vertical, weather, Pane::NflPane)
                    .unwrap();
                panes.split(pane_grid::Axis::Horizontal, nfl, Pane::MlbPane);
                panes
            },
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
    period: u8,
}

impl Game {
    fn new(sport: Sport, team1: &str, team2: &str, score1: &str, score2: &str, period: u8) -> Self {
        Game {
            sport,
            team1: team1.to_string(),
            team2: team2.to_string(),
            score1: score1.to_string(),
            score2: score2.to_string(),
            period,
        }
    }

    fn update(&mut self, score1: &str, score2: &str) {
        self.score1 = score1.to_string();
        self.score2 = score2.to_string();
    }
}

fn sports() -> Vec<Game> {
    println!("Sports!");

    vec![
        Game::new(Sport::NBA, "Lakers", "Warriors", "100", "95", 3),
        Game::new(Sport::NBA, "Celtics", "Nets", "110", "105", 2),
        Game::new(Sport::MLB, "Red Sox", "Yankees", "100", "95", 1),
    ]
}

mod sports_updates {
    use super::Game;
    use super::Sport;

    pub fn update_nba() {
        let nba_games = ureq::get(
            "https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json",
        )
        .header("User-Agent", "deathclock-app/1.0")
        .call()
        .unwrap()
        .into_body()
        .read_to_vec()
        .unwrap();

        let json: serde_json::Value = serde_json::from_slice(&nba_games).unwrap();
        let games = json["scoreboard"]["games"].as_array().unwrap();

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
            game.update(&home_score, &away_score);
            println!("Game ID: {}", game_id);
            println!("Home Team: {}", home_team);
            println!("Away Team: {}", away_team);
            println!("Home Score: {}", home_score);
            println!("Away Score: {}", away_score);
            println!("Period: {}", period);
        }
    }
}
