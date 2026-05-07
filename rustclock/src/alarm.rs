struct Alarm {
    time: chrono::DateTime<chrono::Local>,
    alarm_time_hour: u32,
    alarm_time_minute: u32,
    am_pm: String,
    is_set: bool,
    is_ringing: bool,
}

impl Alarm {
    fn new(time: chrono::DateTime<chrono::Local>, alarm_time_hour: u32, alarm_time_minute: u32, am_pm: String) -> Self {
        Self {
            time,
            alarm_time_hour,
            alarm_time_minute,
            am_pm,
            is_set: true,
            is_ringing: false,
        }
    }
}

