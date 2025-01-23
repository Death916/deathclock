from playwright.sync_api import sync_playwright
import os

class Weather:
    def __init__(self):
        if not os.path.exists('assets'):
            os.makedirs('assets')
            
    def get_weather_screenshot(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
        """)
            page = context.new_page()
            
            # Navigate to Sacramento weather
            page.goto("https://www.bing.com/search?q=sacramento+weather&qs=n&form=QBRE&sp=-1&ghc=1&lq=0&pq=sacramento+weathe&sc=12-17&sk=&cvid=9D84287D34AC483C85F6E3AA7F943C4F&ghsh=0&ghacc=0&ghpl=")
            
            # Wait for and screenshot weather widget
            page.wait_for_selector('#wtr_cardContainer > div.b_antiTopBleed.b_antiSideBleed.b_antiBottomBleed.b_weainner')
            weather_element = page.locator('#wtr_cardContainer > div.b_antiTopBleed.b_antiSideBleed.b_antiBottomBleed.b_weainner')
            screenshot_path = os.path.join('assets', 'sacramento_weather_map.png')
            weather_element.screenshot(path=screenshot_path)
            
            browser.close()
            return screenshot_path
