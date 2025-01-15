import feedparser

class News:
    def __init__(self):
        self._news_dict = {}
        self._news_dict_length = 0
        
    def get_news(self):
        feeds = []
        self._news_dict = {}  # Reset dict each time
        
        # Load RSS feed list
        with open("feeds.txt", "r") as f:
            feeds = [line.strip() for line in f]
            
        # Get latest news from each feed
        for feed in feeds:
            d = feedparser.parse(feed)
            for post in d.entries[:10]:  # Limit to 3 entries per feed
                if self._news_dict_length >= 20:  # Max 20 total entries
                    return self._news_dict
                    
                self._news_dict[post.title] = {
                    'source': d.feed.title,
                    'publish_date': post.published,
                    'headline': post.title,
                    'summary': post.summary
                }
                self._news_dict_length += 1
                # Store last 20 news items in text file

                
                with open("news.txt", "w") as f:
                    for headline in list(self._news_dict.keys())[-20:]:
                        f.write(f"{headline}\n")

                
        return self._news_dict
