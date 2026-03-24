use iced::widget::image::Handle;
use ureq;

pub fn get_weather() -> Option<Handle> {
    let image = ureq::get("https://v2.wttr.in/Sacramento.png?u0")
        .header("User-Agent", "deathclock-app/1.0")
        .call()
        .unwrap()
        .into_body()
        .read_to_vec()
        .unwrap();

    let handle = Some(Handle::from_bytes(image));
    dbg!("updating weather");
    handle
}
