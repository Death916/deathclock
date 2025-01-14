from playwright.sync_api import sync_playwright
import os

class Weather:
    def __init__(self):
        if not os.path.exists('assets'):
            os.makedirs('assets')
            
    def get_weather_screenshot(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Navigate to Sacramento weather
            page.goto("https://www.google.com/search?q=weather+sacramento&hl=en-GB")
            
            # Wait for and screenshot weather widget
            page.wait_for_selector('#wob_wc')
            weather_element = page.locator('#wob_wc')
            screenshot_path = os.path.join('assets', 'sacramento_weather_map.png')
            weather_element.screenshot(path=screenshot_path)
            
            browser.close()
            return screenshot_path
