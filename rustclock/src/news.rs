use rss::Channel;
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::str::FromStr;

pub fn get_news() {
    let feeds = File::open("../feeds.txt");
    let mut feed_vec = Vec::new();
    match feeds {
        Ok(file) => {
            let reader = BufReader::new(file);
            let channel = Channel::read_from(reader);
            if let Ok(channel) = channel {
                println!("Title: {}", channel.title());
                println!("Link: {}", channel.link());
                println!("Description: {}", channel.description());
            } else {
                eprintln!("Error parsing feed: {}", reader);
            }

            for line in reader.lines() {
                if let Ok(feed) = line {
                    dbg!(&feed);
                    feed_vec.push(feed);
                }
            }
        }
        Err(e) => {
            eprintln!("Error opening file: {}", e);
        }
    }

    for feed in feed_vec.iter() {
        let content = feed.as_str();
        dbg!(content);
        let channel = Channel::from_str(content);
        if let Ok(channel) = channel {
            println!("Title: {}", channel.title());
            println!("Link: {}", channel.link());
            println!("Description: {}", channel.description());
        } else {
            eprintln!("Error parsing feed: {}", content);
        }
    }
}

#[test]
fn test() {
    get_news();
}
