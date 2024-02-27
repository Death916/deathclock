from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from PySide6.QtCore import QObject, Signal, Property
import os
from PySide6.QtQuick import QQuickImageProvider
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtQml import QQmlApplicationEngine


class Weather(QObject):
    weatherUpdated = Signal(str)
    def __init__(self):
        
        super().__init__()
        
   
    
    def download_sacramento_weather_map(self,engine):
        url = "https://www.google.com/search?q=weather&hl=en-GB"
        service = Service(executable_path='/home/death916/code/python/deathclock/deathclock/chromedriver')
        options = webdriver.ChromeOptions()
        #options.add_argument('--headless')
        driver = webdriver.Chrome(service=service, options=options)
        options.add_argument('--force-dark-mode')
        driver.get(url)
        map_element = driver.find_element('id', 'wob_wc')
        screenshot_path = 'sacramento_weather_map.png'
        map_element.screenshot(screenshot_path)
        print("screen shot taken")
        
        weather_context = engine.rootContext()
       
        image = screenshot_path
        weather_context = engine.rootContext()
        weather_context.setContextProperty("weatherImage", image)
        driver.quit()
        print("weather updated")
        self.weatherUpdated.emit(image)
        return screenshot_path
    
        def cur_weather():
            # scrape weather from web
            

            pass
    def delete_old_screen_shot(self):
         # delete old screen shot from downloads weather map
        
        file = '/home/death916/code/python/deathclock/sacramento_weather_map.png'
        if os.path.exists(file):
            os.remove(file)
        print("old screen shot deleted")

