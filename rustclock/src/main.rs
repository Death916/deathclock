#![allow(dead_code)]

mod sports;
use chrono::DateTime;
use chrono::Local;
use iced::Border;
use iced::Element;
use iced::Fill;
use iced::widget::{column, container, image, pane_grid, row, scrollable, text};
use sports::Game;
pub fn main() -> iced::Result {
    iced::run(State::update, State::view)
}

#[derive(Debug, Clone)]
enum PaneType {
    MlbPane,
    NflPane,
    NbaPane,
    Weather,
    Clock,
    News,
}

#[derive(Debug, Clone)]
enum Message {
    PaneDragged(pane_grid::DragEvent),
    PaneResized(pane_grid::ResizeEvent),
}

#[derive(Debug)]
struct State {
    current_time: DateTime<Local>,
    next_alarm: Option<DateTime<Local>>,
    news: Vec<String>,
    weather: Vec<u8>,
    location: String,
    nba_scores: Vec<Game>,
    mlb_scores: Vec<Game>,
    // nfl_scores: Vec<Game>,
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
                    let games = &state.nba_scores;
                    column(games.iter().map(|game| {
                        container(
                            column![
                                row![
                                    text(&game.team1).size(20).width(Fill),
                                    text(&game.team2).size(20).width(Fill),
                                ],
                                row![
                                    text(&game.score1).size(20).width(Fill),
                                    text(&game.score2).size(20).width(Fill),
                                ],
                                text(format!("Period: {}", game.period)).size(14),
                            ]
                            .padding(10),
                        )
                        .padding(5)
                        .width(Fill)
                        .style(|_| container::Style {
                            background: Some(iced::Background::Color(iced::Color::from_rgb(
                                0.2, 0.2, 0.2,
                            ))),
                            border: Border {
                                width: 1.0,
                                color: iced::Color::WHITE,
                                radius: 0.0.into(),
                            },
                            text_color: Some(iced::Color::WHITE),
                            snap: true,
                            shadow: iced::Shadow {
                                color: iced::Color::BLACK,
                                offset: iced::Vector::new(0.0, 0.0),
                                blur_radius: 10.0,
                            },
                        })
                        .into()
                    }))
                    .padding(0)
                    .into()
                }
                PaneType::NflPane => text("NFL").into(),
                PaneType::News => text("News").into(),
                PaneType::MlbPane => {
                    let games = &state.mlb_scores;
                    scrollable(column(games.iter().map(|game| {
                        container(
                            column![
                                row![
                                    text(&game.team1).size(20).width(Fill),
                                    text(&game.team2).size(20).width(Fill),
                                ],
                                row![
                                    text(&game.score1).size(20).width(Fill),
                                    text(&game.score2).size(20).width(Fill),
                                ],
                                text(format!("Period: {}", game.period)).size(14),
                            ]
                            .padding(10),
                        )
                        .padding(5)
                        .width(Fill)
                        .style(|_| container::Style {
                            background: Some(iced::Background::Color(iced::Color::from_rgb(
                                0.2, 0.2, 0.2,
                            ))),
                            border: Border {
                                width: 1.0,
                                color: iced::Color::WHITE,
                                radius: 0.0.into(),
                            },
                            text_color: Some(iced::Color::WHITE),
                            snap: true,
                            shadow: iced::Shadow {
                                color: iced::Color::BLACK,
                                offset: iced::Vector::new(0.0, 0.0),
                                blur_radius: 10.0,
                            },
                        })
                        .into()
                    })))
                    .into()
                }
                PaneType::Clock => text("clock").into(),
                PaneType::Weather => {
                    let weather_img = image::Handle::from_bytes(state.weather.clone());
                    let time = Local::now().format("%m/%d %H:%M:%S").to_string();
                    container(
                        column![
                            text(time).size(30),
                            text("Weather").size(50),
                            image(weather_img).width(Fill),
                            text(state.location.clone()).size(30),
                        ]
                        .padding(5),
                    )
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
        sports::update_mlb();

        let text = ureq::get("https://v2.wttr.in/Sacramento.png?u0")
            .header("User-Agent", "deathclock-app/1.0")
            .call()
            .unwrap()
            .into_body()
            .read_to_vec()
            .unwrap();

        State {
            current_time: Local::now(),
            next_alarm: None,
            news: Vec::new(),
            weather: text,
            location: "Sacramento".to_string(),
            nba_scores: { sports::update_nba() },
            mlb_scores: { sports::update_mlb() },
            panes: {
                let (mut panes, nba) = pane_grid::State::new(PaneType::NbaPane);
                let (weather, _) = panes
                    .split(pane_grid::Axis::Vertical, nba, PaneType::Weather)
                    .unwrap();
                let (mlb, _) = panes
                    .split(pane_grid::Axis::Vertical, weather, PaneType::MlbPane)
                    .unwrap();
                panes.split(pane_grid::Axis::Horizontal, mlb, PaneType::NflPane);
                panes
            },
        }
    }
}
