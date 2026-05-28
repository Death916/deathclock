// #![allow(dead_code)]
mod alarm;
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

use iced_webview::{Action, PageType, WebView};
use sports::{Game, Games, Sport};
use std::collections::HashMap;

type Engine = iced_webview::Cef;

const WEATHER_STAR_URL: &str = "https://weatherstar.netbymatt.com/?hazards-checkbox=true&current-weather-checkbox=true&latest-observations-checkbox=true&hourly-checkbox=true&hourly-graph-checkbox=true&travel-checkbox=false&regional-forecast-checkbox=true&local-forecast-checkbox=true&extended-forecast-checkbox=true&almanac-checkbox=true&spc-outlook-checkbox=true&radar-checkbox=true&settings-wide-checkbox=false&settings-kiosk-checkbox=true&settings-stickyKiosk-checkbox=false&settings-customTextEnable-checkbox=false&settings-speed-select=1.00&settings-scanLineMode-select=&settings-units-select=us&txtLocation=Sacramento%2C+CA%2C+USA&settings-customText-string=&share-link-url=&settings-scanLines-checkbox=true&settings-mediaVolume-select=0.75&latLonQuery=Citrus+Heights%2C+CA%2C+USA&latLon=%7B%22lat%22%3A38.6773%2C%22lon%22%3A-121.3006%7D";
const CLOCK_UPDATE_TIME_MS: u64 = 1500;
const UPDATE_SPORTS_TIME_MINS: u64 = 5;
const UPDATE_SPORTS_TIME_OFF_PEAK_MINS: u64 = 30; // TODO!   add this
const WEATHER_UPDATE_TIME_MINS: u64 = 15; // increase when done testing
const NEWS_UPDATE_TIME_MINS: u64 = 15;
const NEWS_ROTATE_TIME_SECS: u64 = 15;
const WEATHER_TYPE: WeatherType = WeatherType::WeatherStar;

pub fn main() -> iced::Result {
    if iced_webview::cef_subprocess_check() {
        return Ok(());
    }
    iced::application(
        || {
            let mut tasks = vec![Task::perform(news::get_news(), Message::UpdateNews)];

            match WEATHER_TYPE {
                WeatherType::WeatherStar => {
                    tasks.push(Task::done(Message::WebView(Action::CreateView(
                        PageType::Url(WEATHER_STAR_URL.to_string()),
                    ))));
                }
                WeatherType::Wttr => {
                    tasks.push(Task::perform(
                        weather::get_weather_image(),
                        Message::UpdateWeatherImg,
                    ));
                }
            }

            (RustClock::default(), Task::batch(tasks))
        },
        RustClock::update,
        RustClock::view,
    )
    .title("RustClock")
    .subscription(RustClock::subscription)
    .theme(|state: &RustClock| state.theme.clone())
    .run()
}

#[derive(Debug, Clone)]
enum PaneType {
    SportsPane(Sport),
    SportsPaneLeft(Sport),
    SportsPaneRight(Sport),
    Weather,
    Clock,
    News,
}

#[derive(Debug, Clone, PartialEq)]
enum WeatherType {
    Wttr,
    WeatherStar,
}

#[derive(Debug, Clone)]
enum Message {
    PaneDragged(pane_grid::DragEvent),
    PaneResized(pane_grid::ResizeEvent),
    RunSportsUpdate,
    UpdateTime,
    RunWeatherUpdate,
    UpdateWeatherImg(Handle),
    RunNewsUpdate,
    UpdateNews(Vec<String>),
    IncNewsIndex,
    ViewCreated,
    WebView(Action),
}

struct RustClock {
    current_time: DateTime<Local>,
    next_alarm: Option<DateTime<Local>>,
    news: Vec<String>,
    news_index: usize,
    location: String,
    all_games: Games,
    nba_scores: Vec<Game>,
    mlb_scores: Vec<Game>,
    panes: pane_grid::State<PaneType>,
    nba_logos: HashMap<String, Handle>,
    mlb_logos: HashMap<String, Handle>,
    weather_handle: Option<Handle>,
    theme: iced::Theme,
    weather_type: WeatherType,
    webview: Option<WebView<Engine, Message>>,
    ready: bool,
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
                self.all_games = Games::update_games(self.all_games.clone());
                self.nba_scores = self.all_games.nba.clone();
                self.mlb_scores = self.all_games.mlb.clone();
                Task::none()
            }
            Message::UpdateTime => {
                self.current_time = Local::now();
                Task::none()
            }
            Message::RunWeatherUpdate => {
                if self.weather_type == WeatherType::Wttr {
                    Task::perform(weather::get_weather_image(), Message::UpdateWeatherImg)
                } else {
                    Task::none()
                }
            }
            Message::UpdateWeatherImg(handle) => {
                self.weather_handle = Some(handle);
                Task::none()
            }

            Message::RunNewsUpdate => Task::perform(news::get_news(), Message::UpdateNews),

            Message::UpdateNews(news) => {
                self.news = news;
                Task::none()
            }
            Message::IncNewsIndex => {
                if !self.news.is_empty() {
                    self.news_index = (self.news_index + 1) % self.news.len();
                }
                Task::none()
            }
            Message::WebView(action) => {
                if let Some(webview) = &mut self.webview {
                    webview.update(action)
                } else {
                    println!("WebView Warning: Received action but webview is None");
                    Task::none()
                }
            }
            Message::ViewCreated => {
                println!("WebView: ViewCreated message received");
                self.ready = true;
                if let Some(webview) = &mut self.webview {
                    webview.update(Action::ChangeView(0))
                } else {
                    println!("WebView Error: ViewCreated received but webview is None");
                    Task::none()
                }
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
            iced::time::every(Duration::from_mins(NEWS_UPDATE_TIME_MINS))
                .map(|_| Message::RunNewsUpdate),
            iced::time::every(Duration::from_secs(NEWS_ROTATE_TIME_SECS))
                .map(|_| Message::IncNewsIndex),
            iced::time::every(Duration::from_millis(30))
                .map(|_| Action::Update)
                .map(Message::WebView),
        ])
    }

    fn view(state: &RustClock) -> Element<'_, Message> {
        pane_grid(&state.panes, |_panes, pane_state, _is_maximized| {
            let content: Element<'_, Message> = match pane_state {
                PaneType::SportsPane(Sport::NBA) => {
                    panes::render_sports_pane(Sport::NBA, &state.nba_scores, &state.nba_logos)
                }
                PaneType::SportsPane(Sport::NFL) => panes::render_nfl_pane(),
                PaneType::News => panes::render_news_pane(&state.news, state.news_index),
                PaneType::SportsPane(Sport::MLB) => {
                    panes::render_sports_pane(Sport::MLB, &state.mlb_scores, &state.mlb_logos)
                }
                PaneType::SportsPaneLeft(sport) => {
                    let full_games: &[Game] = match sport {
                        Sport::NBA => &state.nba_scores,
                        Sport::MLB => &state.mlb_scores,
                        Sport::NFL => &[],
                    };
                    let mid = full_games.len() / 2;
                    let (left, _) = full_games.split_at(mid);
                    let logos = match sport {
                        Sport::NBA => &state.nba_logos,
                        Sport::MLB => &state.mlb_logos,
                        Sport::NFL => &state.mlb_logos, // placeholder for NFL
                    };
                    panes::render_sports_pane(sport.clone(), left, logos)
                }
                PaneType::SportsPaneRight(sport) => {
                    let full_games: &[Game] = match sport {
                        Sport::NBA => &state.nba_scores,
                        Sport::MLB => &state.mlb_scores,
                        Sport::NFL => &[],
                    };
                    let mid = full_games.len() / 2;
                    let (_, right) = full_games.split_at(mid);
                    let logos = match sport {
                        Sport::NBA => &state.nba_logos,
                        Sport::MLB => &state.mlb_logos,
                        Sport::NFL => &state.mlb_logos, // placeholder for NFL
                    };
                    panes::render_sports_pane(sport.clone(), right, logos)
                }
                PaneType::Clock => panes::render_clock_pane(),
                PaneType::Weather => match state.weather_type {
                    WeatherType::WeatherStar => panes::render_weather_star_pane(state),
                    WeatherType::Wttr => {
                        panes::render_wttr_pane(&state.weather_handle, &state.location)
                    }
                },
            };
            pane_grid::Content::new(content)
        })
        .on_drag(Message::PaneDragged)
        .on_resize(10, Message::PaneResized)
        .into()
    }
}

fn create_config(sports: &Games) -> Configuration<PaneType> {
    let default_config = Configuration::Split {
        axis: pane_grid::Axis::Horizontal,
        ratio: 0.05,
        a: Box::new(Configuration::Pane(PaneType::Clock)),
        b: Box::new(Configuration::Split {
            axis: pane_grid::Axis::Vertical,
            ratio: 0.25,
            a: Box::new(Configuration::Pane(PaneType::SportsPane(Sport::NBA))),
            b: Box::new(Configuration::Split {
                axis: pane_grid::Axis::Vertical,
                ratio: 0.66,
                a: Box::new(Configuration::Split {
                    axis: pane_grid::Axis::Horizontal,
                    ratio: 0.85,
                    a: Box::new(Configuration::Pane(PaneType::Weather)),
                    b: Box::new(Configuration::Pane(PaneType::News)),
                }),
                b: Box::new(Configuration::Split {
                    axis: pane_grid::Axis::Horizontal,
                    ratio: 0.85, //fix later when all sports active TODO
                    a: Box::new(Configuration::Pane(PaneType::SportsPane(Sport::MLB))),
                    b: Box::new(Configuration::Pane(PaneType::SportsPane(Sport::NFL))),
                }),
            }),
        }),
    };

    let mut active_sports = Vec::new();
    if sports.is_active(Sport::NBA) {
        active_sports.push(Sport::NBA);
    }
    if sports.is_active(Sport::NFL) {
        active_sports.push(Sport::NFL);
    }
    if sports.is_active(Sport::MLB) {
        active_sports.push(Sport::MLB);
    }

    if active_sports.len() == 1 {
        let sport = active_sports[0].clone();
        Configuration::Split {
            axis: pane_grid::Axis::Horizontal,
            ratio: 0.05,
            a: Box::new(Configuration::Pane(PaneType::Clock)),
            b: Box::new(Configuration::Split {
                axis: pane_grid::Axis::Vertical,
                ratio: 0.25,
                a: Box::new(Configuration::Pane(PaneType::SportsPaneLeft(sport.clone()))),
                b: Box::new(Configuration::Split {
                    axis: pane_grid::Axis::Vertical,
                    ratio: 0.66,
                    a: Box::new(Configuration::Split {
                        axis: pane_grid::Axis::Horizontal,
                        ratio: 0.85,
                        a: Box::new(Configuration::Pane(PaneType::Weather)),
                        b: Box::new(Configuration::Pane(PaneType::News)),
                    }),
                    b: Box::new(Configuration::Split {
                        axis: pane_grid::Axis::Horizontal,
                        ratio: 0.85,
                        a: Box::new(Configuration::Pane(PaneType::SportsPaneRight(
                            sport.clone(),
                        ))),
                        b: Box::new(Configuration::Pane(PaneType::SportsPane(Sport::NFL))),
                    }),
                }),
            }),
        }
    } else {
        default_config
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

        let weather_type = WEATHER_TYPE;
        let webview = match weather_type {
            WeatherType::WeatherStar => Some(
                WebView::new()
                    .on_create_view(Message::ViewCreated)
                    .on_action(Message::WebView),
            ),
            WeatherType::Wttr => None,
        };

        let games_list = Games::new();
        let config = create_config(&games_list);

        RustClock {
            current_time: Local::now(),
            next_alarm: None,
            news: Vec::new(),
            news_index: 0,
            location: "Sacramento".to_string(),
            all_games: games_list.clone(),
            nba_scores: games_list.nba,
            mlb_scores: games_list.mlb,
            mlb_logos,
            nba_logos,
            weather_handle: None,
            theme: iced::Theme::TokyoNight,
            weather_type,
            webview,
            ready: false,
            panes: { pane_grid::State::with_configuration(config) },
        }
    }
}
