import datetime
import asyncio
from dash import html, Input, Output, callback, no_update
from dash.exceptions import PreventUpdate
from news import News

class NewsModule:
    def __init__(self, app):
        self.app = app
        self.news_obj = self.get_news_object()
        self._last_news_update = datetime.datetime(2000, 1, 1)
        self._cached_news = self.create_loading_message()  # Initial loading message
        self._initial_run = True
        self.setup_callbacks()

    def get_news_object(self):
        return News()

    def create_loading_message(self):
        return html.Div("Loading...")

    def setup_callbacks(self):
        @self.app.callback(
            Output('news-ticker', 'children'),
            Input('news-interval', 'n_intervals')
        )
        def update_news(n):
            if n is None:
                return self._cached_news
                
            current_time = datetime.datetime.now()
            try:
                print("UPDATING NEWS...")
                # Execute the async function with asyncio.run
                headlines_dict = asyncio.run(self.news_obj.get_news())
                
                combined_items = " | ".join([f"{data['source']}: {headline}" 
                                           for headline, data in headlines_dict.items()])
                text_px = len(combined_items) * 8
                scroll_speed = 75
                duration = max(text_px / scroll_speed, 20)
                ticker_style = {"animationDuration": f"{duration}s"}
                
                self._cached_news = html.Div(
                    html.Span(combined_items, className="news-item", style=ticker_style),
                    className='ticker'
                )
                
                self._last_news_update = current_time
                self._initial_run = False
                return self._cached_news
            except Exception as e:
                print(f"Error updating news: {e}")
                return html.Div("No news available.")
