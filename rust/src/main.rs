mod sports;
use iced::Center;
use iced::Element;
use iced::widget::{column, image, pane_grid, row, text};
use sports::Game;
pub fn main() -> iced::Result {
    iced::run(State::update, State::view)
}

#[derive(Debug, Clone)]
enum PaneType {
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
    panes: pane_grid::State<PaneType>,
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
        pane_grid(&state.panes, |_panes, pane_state, _is_maximized| {
            let content: Element<'_, Message> = match pane_state {
                PaneType::NbaPane => {
                    let games = &state.scores;
                    column![
                        text("NBA").size(50),
                        text(format!("{} vs {}", games[0].team1, games[0].team2)).size(20),
                        text(format!("{} - {}", games[0].score1, games[0].score2)).size(20),
                    ]
                    .padding(5)
                    .into()
                }
                PaneType::NflPane => text("NFL").into(),
                PaneType::MlbPane => text("MLB").into(),
                PaneType::Main => text("Main").into(),
                PaneType::Weather => {
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
                sports::update_nba();
                sports::sports()
            },
            panes: {
                let (mut panes, nba) = pane_grid::State::new(PaneType::NbaPane);
                let (weather, _) = panes
                    .split(pane_grid::Axis::Vertical, nba, PaneType::Weather)
                    .unwrap();
                let (nfl, _) = panes
                    .split(pane_grid::Axis::Vertical, weather, PaneType::NflPane)
                    .unwrap();
                panes.split(pane_grid::Axis::Horizontal, nfl, PaneType::MlbPane);
                panes
            },
        }
    }
}
