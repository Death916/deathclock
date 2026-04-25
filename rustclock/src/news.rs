use rss::Channel;
use std::fs::File;
use std::io::{BufRead, BufReader};

pub async fn get_news() -> Vec<String> {
    let feeds = File::open("../feeds.txt");
    let mut source_feed_vec = Vec::new();
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
        dbg!(feed_url);
        let content = reqwest::get(feed_url).await;

        match content {
            Ok(contents) => {
                let contents = contents.bytes().await;
                if let Ok(response) = contents {
                    let channel = Channel::read_from(&response[..]);
                    // dbg!(&channel);
                    match channel {
                        Ok(feed) => {
                            let channel_title = feed.title().to_string();
                            let items = feed.into_items();
                            for item in items.iter().take(10) {
                                let title = item.title();
                                if let Some(title) = title {
                                    let headline = format!("{}: {}", channel_title, title);
                                    news.push(headline);
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

pub fn get_news_item(index: usize, news_feeds: &Vec<String>) -> String {
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
        let news_item = get_news_item(index, &news);
        dbg!(news_item);
    }
}
