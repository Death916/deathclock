// #![allow(dead_code)]
mod news;
mod panes;
mod sports;
mod weather;
use chrono::{DateTime, Local};
use iced::Element;
use iced::Subscription;
use iced::Task;
use iced::time::Duration;
use iced::widget::image::Handle;
use iced::widget::pane_grid;
use iced::widget::pane_grid::Configuration;
use sports::Game;
use std::collections::HashMap;

const CLOCK_UPDATE_TIME_MS: u64 = 1500;
const UPDATE_SPORTS_TIME_MINS: u64 = 5;
const WEATHER_UPDATE_TIME_MINS: u64 = 30;

pub fn main() -> iced::Result {
    iced::application(
        || (RustClock::default(), Task::perform(weather::get_weather(), Message::UpdateWeatherImg)), // Wrap it in a closure
        RustClock::update,
        RustClock::view,
    )
    .title("RustClock")
    .subscription(RustClock::subscription)
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
    UpdateTime,
    RunWeatherUpdate,
    UpdateWeatherImg(Handle),
}

#[derive(Debug)]
struct RustClock {
    current_time: DateTime<Local>,
    next_alarm: Option<DateTime<Local>>,
    news: Vec<String>,
    location: String,
    nba_scores: Vec<Game>,
    mlb_scores: Vec<Game>,
    panes: pane_grid::State<PaneType>,
    nba_logos: HashMap<String, Handle>,
    mlb_logos: HashMap<String, Handle>,
    weather_handle: Option<Handle>,
}
impl RustClock {
    fn update(&mut self, message: Message) -> iced::Task<Message> {
        match message {
            Message::PaneDragged(pane_grid::DragEvent::Dropped { pane, target }) => {
                self.panes.drop(pane, target);
                Task::none()
            }
            Message::PaneDragged(_) => Task::none(),
            
            Message::PaneResized(pane_grid::ResizeEvent { split, ratio }) => {
                self.panes.resize(split, ratio);
                Task::none()
            }
            Message::RunSportsUpdate => {
                self.nba_scores = sports::update_nba();
                self.mlb_scores = sports::update_mlb();
                Task::none()
            }
            Message::UpdateTime => {
                self.current_time = Local::now();
                Task::none()
            }
            Message::RunWeatherUpdate => Task::perform(weather::get_weather(), Message::UpdateWeatherImg),
            Message::UpdateWeatherImg(handle) => {
                self.weather_handle = Some(handle);
                Task::none()
            }
        }
    }

    fn subscription(&self) -> Subscription<Message> {
        Subscription::batch(vec![
            iced::time::every(Duration::from_millis(CLOCK_UPDATE_TIME_MS))
                .map(|_| Message::UpdateTime),
            iced::time::every(Duration::from_mins(UPDATE_SPORTS_TIME_MINS))
                .map(|_| Message::RunSportsUpdate),
            iced::time::every(Duration::from_mins(WEATHER_UPDATE_TIME_MINS))
                .map(|_| Message::RunWeatherUpdate),
        ])
    }

    fn view(state: &RustClock) -> Element<'_, Message> {
        pane_grid(&state.panes, |_panes, pane_state, _is_maximized| {
            let content: Element<'_, Message> = match pane_state {
                PaneType::NbaPane => panes::render_nba_pane(&state.nba_scores, &state.nba_logos),
                PaneType::NflPane => panes::render_nfl_pane(),
                PaneType::News => panes::render_news_pane(),
                PaneType::MlbPane => panes::render_mlb_pane(&state.mlb_scores, &state.mlb_logos),
                PaneType::Clock => panes::render_clock_pane(),
                PaneType::Weather => {
                    panes::render_weather_pane(&state.weather_handle, &state.location)
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
        let mlb_logos_bytes = sports::get_mlb_logos();
        let nba_logos_bytes = sports::get_nba_logos();

        let mlb_logos: HashMap<String, Handle> = mlb_logos_bytes
            .into_iter()
            .map(|(k, v)| (k, Handle::from_bytes(v)))
            .collect();
        let nba_logos: HashMap<String, Handle> = nba_logos_bytes
            .into_iter()
            .map(|(k, v)| (k, Handle::from_bytes(v)))
            .collect();
        

        RustClock {
            current_time: Local::now(),
            next_alarm: None,
            news: Vec::new(),
            location: "Sacramento".to_string(),
            nba_scores: { sports::update_nba() },
            mlb_scores: { sports::update_mlb() },
            mlb_logos,
            nba_logos,
            weather_handle: None,
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
