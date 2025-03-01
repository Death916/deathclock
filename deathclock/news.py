import feedparser
import asyncio
import aiofiles
import random
from time import localtime, strftime
import socket
import aiohttp

def print_time():
    print(strftime("%B %d, %I:%M %p", localtime()))

class News:
    def __init__(self):
        self._news_dict = {}
        self._news_dict_length = 0
        socket.setdefaulttimeout(10)  # Set default timeout for socket operations

    async def _fetch_feed(self, session, feed):
        """Fetches and parses a single feed asynchronously."""
        max_entries = 10  # Maximum number of entries to fetch from each feed
        try:
            async with session.get(feed) as response:
                if response.status != 200:
                    print(f"Skip feed {feed}: status {response.status}")
                    return []
                text = await response.text()
                d = feedparser.parse(text)

                if hasattr(d, 'status') and d.status != 200:
                    print(f"Skip feed {feed}: status {d.status}")
                    return []

                feed_entries = []
                # Limit the number of entries parsed
                for i, post in enumerate(d.entries):
                    if i >= max_entries:
                        break  # Stop parsing if we've reached the limit
                    feed_entries.append({
                        'title': post.title,
                        'source': d.feed.title if hasattr(d.feed, 'title') else 'Unknown',
                        'publish_date': post.published if hasattr(post, 'published') else '',
                        'summary': post.summary if hasattr(post, 'summary') else ''
                    })
                print(f"Added {len(feed_entries)} entries from {feed}")
                return feed_entries

        except aiohttp.ClientError as e:
            print(f"Error processing feed {feed}: {e}")
            return []
        except Exception as e:
            print(f"Error processing feed {feed}: {e}")
            return []

    async def get_news(self):
        print_time()
        feeds = []
        self._news_dict = {}
        self._news_dict_length = 0

        try:
            async with aiofiles.open("feeds.txt", "r") as f:
                async for line in f:
                    feeds.append(line.strip())
        except Exception as e:
            print(f"Error reading feeds.txt: {e}")
            return {}

        print("Getting news entries...")
        async with aiohttp.ClientSession() as session:
            tasks = [self._fetch_feed(session, feed) for feed in feeds]
            all_feed_entries_list = await asyncio.gather(*tasks)

        all_entries = []
        for feed_entries in all_feed_entries_list:
            if feed_entries:
                #Now just add the entries, because we are already limited
                all_entries.extend(feed_entries)

        if not all_entries:
            print("No entries collected")
            return {}
        
        if len(all_entries) > 30:
            all_entries = random.sample(all_entries, 30)

        for entry in all_entries:
            self._news_dict[entry['title']] = entry

        try:
            async with aiofiles.open("news.txt", "w") as f:
                print("Writing news to file...")
                for entry in self._news_dict.values():
                    await f.write(f"[{entry['publish_date']}] {entry['source']}: {entry['title']}\n")
        except Exception as e:
            print(f"Error writing to news.txt: {e}")

        return self._news_dict
