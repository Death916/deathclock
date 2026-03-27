use rss::{Channel, Item};
use std::fs::File;
use std::io::{BufRead, BufReader};

pub async fn get_news() -> Vec<String> {
    let feeds = File::open("../feeds.txt");
    let mut source_feed_vec = Vec::new();
    let mut channel_vec: Vec<Channel> = Vec::new();
    let mut news = Vec::new();
    match feeds {
        Ok(file) => {
            let reader = BufReader::new(file);
            for line in reader.lines() {
                if let Ok(feed) = line {
                    source_feed_vec.push(feed);
                }
            }
        }
        Err(e) => {
            eprintln!("Error opening file: {}", e);
        }
    }

    for feed in source_feed_vec.iter() {
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
                            channel_vec.push(feed);
                            for source in channel_vec.iter().map(|item| item.clone().into_items()) {
                                for feed in source[1..].iter() {
                                    let source = feed.title();
                                    if let Some(source) = source {
                                        let headline = source.to_string();
                                        news.push(headline);
                                    }
                                }
                            }
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

pub async fn get_news_item(index: usize, news_feeds: Vec<String>) -> String {
    if let Some(headline) = news_feeds.get(index) {
        let headline = headline.to_string();
        headline
    } else {
        let error_message = format!("could not find news item at index {}", index);
        error_message
    }
}

mod tests {
    use super::*;

    #[tokio::test]
    async fn test_get_feeds() {
        let news = get_news().await;
        dbg!(news.len());
        assert!(news.len() > 1);
    }

    #[tokio::test]
    async fn test_get_news_item() {
        let index = 2;
        let news = get_news().await;
        let news_item = get_news_item(index, news).await;
        dbg!(news_item);
    }
}

