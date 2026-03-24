use rss::Channel;
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::str::FromStr;
use ureq::http::Response;

pub async fn get_news() -> Vec<Channel> {
    let feeds = File::open("../feeds.txt");
    let mut feed_vec = Vec::new();
    let mut news = Vec::new();
    match feeds {
        Ok(file) => {
            let reader = BufReader::new(file);
            for line in reader.lines() {
                if let Ok(feed) = line {
                    feed_vec.push(feed);
                }
            }
        }
        Err(e) => {
            eprintln!("Error opening file: {}", e);
        }
    }

    for feed in feed_vec.iter() {
        let feed_url = feed.as_str();
        let content = reqwest::get(feed_url).await;

        match content {
            Ok(contents) => {
                let contents = contents.bytes().await;
                if let Ok(response) = contents {
                    let channel = Channel::read_from(&response[..]);
                    // dbg!(&channel);
                    match channel {
                        Ok(feed) => {
                            dbg!("Title: {}", feed.title());
                            dbg!("Link: {}", feed.link());
                            news.push(feed);
                        }
                        Err(e) => {
                            eprintln!("Error parsing feed: {},{}", feed_url, e);
                        }
                    }
                }
            }

            Err(e) => {
                eprintln!("Error fetching feed: {},{}", feed_url, e);
                continue;
            }
        }
    }
    news
}

#[tokio::test]
async fn test() {
    let news = get_news().await;
    assert!(news.len() > 0);
}
