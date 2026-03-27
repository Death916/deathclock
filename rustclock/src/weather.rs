use iced::widget::image::Handle;
use reqwest;

pub async fn get_weather() -> Handle {
    let image = reqwest::get("https://v2.wttr.in/Sacramento.png?u0")
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

mod tests {
    use super::*;

    #[tokio::test]
    async fn test_get_weather() {
        let handle = get_weather().await;
        let handle_type: Handle = handle.clone();
        assert_eq!(handle_type, handle);
    }
}
