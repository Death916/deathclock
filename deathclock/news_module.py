import datetime
from dash import html, Input, Output
from news import News # Import News class

class NewsModule:
    def __init__(self, app):
        self.app = app
        self.news_obj = self.get_news_object()
        self._last_news_update = datetime.datetime(2000, 1, 1)
        self._cached_news = []
        self._initial_run = True
        self.setup_callbacks()

    def get_news_object(self):
        return News()

    def setup_callbacks(self):
        @self.app.callback(
            Output('news-ticker', 'children'),
            Input('news-interval', 'n_intervals')
        )
        def update_news(n):
            current_time = datetime.datetime.now()
            try:
                print("UPDATING NEWS...")
                headlines_dict = self.news_obj.get_news()
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
                if self._cached_news:
                    return self._cached_news
                return html.Div("No news available.")
