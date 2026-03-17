// #![allow(dead_code)]
mod sports;
use chrono::{DateTime, Local};
use iced::Border;
use iced::Element;
use iced::Fill;
use iced::Task;
use iced::application;
use iced::widget::pane_grid::Configuration;
use iced::widget::{column, container, image, pane_grid, row, scrollable, text};
use sports::Game;
use std::collections::HashMap;
use tokio::time::{Duration, sleep};

pub fn main() -> iced::Result {
    iced::application(
        || (RustClock::default(), Task::none()), // Wrap it in a closure
        RustClock::update,
        RustClock::view,
    )
    .title("RustClock")
    .run()
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
    RunSportsUpdate,
}

#[derive(Debug)]
struct RustClock {
    current_time: DateTime<Local>,
    next_alarm: Option<DateTime<Local>>,
    news: Vec<String>,
    weather: Vec<u8>,
    location: String,
    nba_scores: Vec<Game>,
    mlb_scores: Vec<Game>,
    // nfl_scores: Vec<Game>,
    panes: pane_grid::State<PaneType>,
    nba_logos: HashMap<String, Vec<u8>>,
    mlb_logos: HashMap<String, Vec<u8>>,
}
impl RustClock {
    fn update(&mut self, message: Message) {
        match message {
            Message::PaneDragged(pane_grid::DragEvent::Dropped { pane, target }) => {
                self.panes.drop(pane, target);
            }
            Message::PaneDragged(_) => {}
            Message::PaneResized(pane_grid::ResizeEvent { split, ratio }) => {
                self.panes.resize(split, ratio);
            }
            Message::RunSportsUpdate => {
                self.nba_scores = sports::update_nba();
                self.mlb_scores = sports::update_mlb();
            }
        }
    }

    fn view(state: &RustClock) -> Element<'_, Message> {
        pane_grid(&state.panes, |_panes, pane_state, _is_maximized| {
            let content: Element<'_, Message> = match pane_state {
                PaneType::NbaPane => {
                    let games = &state.nba_scores;

                    column(games.iter().map(|game| {
                        let Some(team1_logo) = state.nba_logos.get(&game.team1) else {
                            return text(format!(
                                "Error: Team 1 logo not found for {}",
                                game.team1
                            ))
                            .into();
                        };
                        let team1_handle = image::Handle::from_bytes(team1_logo.clone());
                        let Some(team2_logo) = state.nba_logos.get(&game.team2) else {
                            return text("Error: Team 2 logo not found").into();
                        };
                        let team2_handle = image::Handle::from_bytes(team2_logo.clone());

                        container(
                            column![
                                row![
                                    image(team1_handle).width(30).height(30),
                                    text(&game.team1).size(20).width(Fill),
                                    image(team2_handle).width(30).height(30),
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
                    .width(50)
                    .into()
                }
                PaneType::NflPane => text("NFL").into(),
                PaneType::News => text("News").into(),
                PaneType::MlbPane => {
                    let games = &state.mlb_scores;
                    scrollable(column(games.iter().map(|game| {
                        let Some(team1_logo) = state.mlb_logos.get(&game.team1) else {
                            return text(format!(
                                "Error: Team 1 logo not found for {}",
                                game.team1
                            ))
                            .into();
                        };
                        let team1_handle = image::Handle::from_bytes(team1_logo.clone());
                        let Some(team2_logo) = state.mlb_logos.get(&game.team2) else {
                            return text("Error: Team 2 logo not found").into();
                        };
                        let team2_handle = image::Handle::from_bytes(team2_logo.clone());
                        container(
                            column![
                                row![
                                    image(team1_handle.clone()).width(15).height(15),
                                    text(&game.team1).size(20).width(Fill),
                                    image(team2_handle.clone()).width(15).height(15),
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
                PaneType::Clock => container(row![
                    text(Local::now().format("%m/%d %H:%M:%S").to_string()).size(30),
                ])
                .align_x(iced::Alignment::Center)
                .into(),
                PaneType::Weather => {
                    let weather_img = image::Handle::from_bytes(state.weather.clone());
                    container(
                        column![
                            text("Weather").size(50),
                            image(weather_img).width(Fill),
                            text(state.location.clone()).size(30),
                        ]
                        .padding(5)
                        .align_x(iced::Alignment::Center),
                    )
                    .width(Fill)
                    .height(Fill)
                    .center_x(Fill)
                    .center_y(Fill)
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

impl Default for RustClock {
    fn default() -> Self {
        sports::get_mlb_logos();

        let text = ureq::get("https://v2.wttr.in/Sacramento.png?u0")
            .header("User-Agent", "deathclock-app/1.0")
            .call()
            .unwrap()
            .into_body()
            .read_to_vec()
            .unwrap();

        let mlb_logos = sports::get_mlb_logos();
        let nba_logos = sports::get_nba_logos();

        RustClock {
            current_time: Local::now(),
            next_alarm: None,
            news: Vec::new(),
            weather: text,
            location: "Sacramento".to_string(),
            nba_scores: { sports::update_nba() },
            mlb_scores: { sports::update_mlb() },
            mlb_logos,
            nba_logos,
            panes: {
                let config = Configuration::Split {
                    axis: pane_grid::Axis::Horizontal,
                    ratio: 0.05,
                    a: Box::new(Configuration::Pane(PaneType::Clock)),
                    b: Box::new(Configuration::Split {
                        axis: pane_grid::Axis::Vertical,
                        ratio: 0.25,
                        a: Box::new(Configuration::Pane(PaneType::NbaPane)),
                        b: Box::new(Configuration::Split {
                            axis: pane_grid::Axis::Vertical,
                            ratio: 0.65,
                            a: Box::new(Configuration::Pane(PaneType::Weather)),
                            b: Box::new(Configuration::Split {
                                axis: pane_grid::Axis::Horizontal,
                                ratio: 0.7,
                                a: Box::new(Configuration::Pane(PaneType::MlbPane)),
                                b: Box::new(Configuration::Pane(PaneType::NflPane)),
                            }),
                        }),
                    }),
                };

                pane_grid::State::with_configuration(config)
            },
        }
    }
}

async fn dash_updates() {
    loop {
        let mut state = RustClock::default();
        state.update(Message::RunSportsUpdate);
        println!("Updated sports scores");
        tokio::time::sleep(Duration::from_secs(60)).await;
    }
}
