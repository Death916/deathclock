use chrono::Local;
use iced::Border;
use iced::Element;
use iced::Fill;
use iced::widget::scrollable::{Direction, Scrollbar};
use iced::widget::{column, container, image, row, scrollable, text};
use std::collections::HashMap;

use crate::Message;
use crate::sports::Game;

use iced::widget::image::Handle;

pub fn render_nba_pane<'a>(
    games: &'a [Game],
    logos: &'a HashMap<String, Handle>,
) -> Element<'a, Message> {
    scrollable(column(games.iter().map(|game| {
        let Some(team1_logo) = logos.get(&game.team1) else {
            return text(format!("Error: Team 1 logo not found for {}", game.team1)).into();
        };
        let Some(team2_logo) = logos.get(&game.team2) else {
            return text("Error: Team 2 logo not found").into();
        };

        container(
            column![
                row![
                    image(team1_logo.clone()).width(30).height(30),
                    text(&game.team1).size(20).width(Fill),
                    image(team2_logo.clone()).width(30).height(30),
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
    .direction(Direction::Vertical(Scrollbar::hidden()))
    .width(50)
    .into()
}

pub fn render_nfl_pane<'a>() -> Element<'a, Message> {
    text("NFL").into()
}

pub fn render_news_pane<'a>() -> Element<'a, Message> {
    
}

pub fn render_mlb_pane<'a>(
    games: &'a [Game],
    logos: &'a HashMap<String, Handle>,
) -> Element<'a, Message> {
    scrollable(column(games.iter().map(|game| {
        let Some(team1_logo) = logos.get(&game.team1) else {
            return text(format!("Error: Team 1 logo not found for {}", game.team1)).into();
        };
        let Some(team2_logo) = logos.get(&game.team2) else {
            return text("Error: Team 2 logo not found").into();
        };
        container(
            column![
                row![
                    image(team1_logo.clone()).width(30).height(30),
                    text(&game.team1).size(20).width(Fill),
                    image(team2_logo.clone()).width(30).height(30),
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
    .direction(Direction::Vertical(Scrollbar::hidden()))
    .into()
}

pub fn render_clock_pane<'a>() -> Element<'a, Message> {
    container(row![
        text(Local::now().format("%m/%d %H:%M:%S").to_string()).size(30)
    ])
    .align_x(iced::Alignment::Center)
    .into()
}

pub fn render_weather_pane<'a>(
    weather_handle: &'a Option<Handle>,
    location: &'a str,
) -> Element<'a, Message> {
    let Some(weather_img) = weather_handle else {
        return text("Weather image not loaded").into();
    };
    container(
        column![
            text("Weather").size(50),
            image(weather_img.clone()).width(Fill),
            text(location).size(30),
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
