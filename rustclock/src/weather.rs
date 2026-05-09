use iced::widget::image::Handle;
use reqwest::Client;

enum WeatherType {
    Wttr,
    WeatherStar,
}

pub async fn get_weather_image() -> Handle {
    let client = Client::builder()
        .user_agent("deathclock-app/1.0")
        .build()
        .unwrap();

    
    let image = client
        .get("https://wttr.in/Sacramento.png?")
        .send()
        .await
        .unwrap()
        .bytes()
        .await
        .unwrap();

    let handle = Some(Handle::from_bytes(image));
    let handle = handle.unwrap();
    //TODO better error handling
    dbg!(format!("{}: updating weather", chrono::Local::now()));
    handle
}

pub async fn get_weatherstar()

mod tests {
    use super::*;

    #[tokio::test]
    async fn test_get_weather() {
        let handle = get_weather_image().await;
        let handle_type: Handle = handle.clone();
        assert_eq!(handle_type, handle);
    }
}
