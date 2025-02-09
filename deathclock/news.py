import feedparser
from time import localtime, strftime
import random
import socket

def print_time():
    print(strftime("%B %d, %I:%M %p", localtime()))

class News:
    def __init__(self):
        self._news_dict = {}
        self._news_dict_length = 0
        # Set timeout for feed fetching
        socket.setdefaulttimeout(10)
        
    def get_news(self):
        print_time()
        feeds = []
        self._news_dict = {}
        self._news_dict_length = 0
        
        try:
            with open("feeds.txt", "r") as f:
                feeds = [line.strip() for line in f]
        except Exception as e:
            print(f"Error reading feeds.txt: {e}")
            return {}
        
        all_entries = []
        print("Getting news entries...")
        
        for feed in feeds:
            try:
                feed_entries = []
                print(f"Fetching from feed: {feed}")  # Debug print
                d = feedparser.parse(feed)
                
                if hasattr(d, 'status') and d.status != 200:
                    print(f"Skip feed {feed}: status {d.status}")
                    continue
                    
                for post in d.entries:
                    feed_entries.append({
                        'title': post.title,
                        'source': d.feed.title if hasattr(d.feed, 'title') else 'Unknown',
                        'publish_date': post.published if hasattr(post, 'published') else '',
                        'summary': post.summary if hasattr(post, 'summary') else ''
                    })
                
                if feed_entries:
                    selected = random.sample(feed_entries, min(10, len(feed_entries)))
                    all_entries.extend(selected)
                    print(f"Added {len(selected)} entries from {feed}")  # Debug print
                
                if len(all_entries) >= 30:
                    break
                    
            except Exception as e:
                print(f"Error processing feed {feed}: {e}")
                continue
        
        if not all_entries:
            print("No entries collected")
            return {}
            
        if len(all_entries) > 30:
            all_entries = random.sample(all_entries, 30)
        
        for entry in all_entries:
            self._news_dict[entry['title']] = entry
        
        try:
            with open("news.txt", "w") as f:
                print("Writing news to file...")
                for entry in self._news_dict.values():
                    f.write(f"[{entry['publish_date']}] {entry['source']}: {entry['title']}\n")
                    f.flush()
        except Exception as e:
            print(f"Error writing to news.txt: {e}")
        
        return self._news_dict
