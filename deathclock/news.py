#news.py
# News module for DeathClock

import feedparser

class news():
    
    def __init__(self):
        self._news = ""
        self._news_list = []
        self._news_list_index = 0
        self._news_list_length = 0
        self._news_list_index_max = 0
        self._news_dict = {}
        self._news_dict_length = 0
    
    def get_news(self):
        feeds = []
        #load rss feed list from file
        with open("feeds.txt", "r") as f:
            for line in f:
                feeds.append(line.strip())
        #print source and headline from last 10 entries
        for feed in feeds:
            d = feedparser.parse(feed)
            for post in d.entries:
                if self._news_list_length == 10:
                    self._news_list.pop(0)
                    self._news_list.append(post.title)
                    
                self._news_list.append(post.title)
                self._news_list_length += 1
                # only store last 20 entries in dict
                if self._news_dict_length == 20:
                    self._news_dict = {}
                self._news_dict[post.title] = {
                    'source': d.feed.title,
                    'publish_date': post.published,
                    'headline': post.title,
                    'summary': post.summary
                }
                self._news_dict_length += 1
                #for i in self._news_dict:
                #    print(self._news_dict[i])
        return self._news_dict


def main():
    news_obj = news()
    news_obj.get_news()
    print(news_obj._news_dict)
    return news_obj._news_dict

if __name__ == "__main__":
    main()


#TODO hash the news_dict and compare to previous hash to see if news has changed
#TODO add news to qml
#TODO limit entries from each source to some number mayb 3ish