// #![allow(dead_code)]
mod panes;
mod sports;
use chrono::{DateTime, Local};
use iced::Element;
use iced::Task;
use iced::application;
use iced::widget::pane_grid;
use iced::widget::pane_grid::Configuration;
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
                PaneType::NbaPane => panes::render_nba_pane(&state.nba_scores, &state.nba_logos),
                PaneType::NflPane => panes::render_nfl_pane(),
                PaneType::News => panes::render_news_pane(),
                PaneType::MlbPane => panes::render_mlb_pane(&state.mlb_scores, &state.mlb_logos),
                PaneType::Clock => panes::render_clock_pane(),
                PaneType::Weather => panes::render_weather_pane(&state.weather, &state.location),
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
