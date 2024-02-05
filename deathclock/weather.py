from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from PySide6.QtCore import QObject, Signal, Property
import os
from PySide6.QtQuick import QQuickImageProvider
from PySide6.QtGui import QImage, QPixmap

class weather():
    
   
    
    def download_sacramento_weather_map(self):
        url = "https://www.google.com/search?q=weather&hl=en-GB"
        service = Service(executable_path='/home/death916/code/python/deathclock/deathclock/chromedriver')
        options = webdriver.ChromeOptions()
        #options.add_argument('--headless')
        driver = webdriver.Chrome(service=service, options=options)
        options.add_argument('--force-dark-mode')
        driver.get(url)
        map_element = driver.find_element('id', 'wob_wc')
        image = map_element.screenshot('sacramento_weather_map.png')
        print("screen shot taken")
        self.image_provider.source = 'sacramento_weather_map.png'
        
        driver.quit()
        return image

        def cur_weather():
            # scrape weather from web
            

            pass
    def delete_old_screen_shot(self):
         # delete old screen shot from downloads weather map
        
        file = '/home/death916/code/python/deathclock/sacramento_weather_map.png'
        if os.path.exists(file):
            os.remove(file)
        print("old screen shot deleted")


class WeatherImageProvider(QQuickImageProvider):
    """weather image provider class to provide image to qml when timer is up"""
    sourceChanged = Signal()
    

    def __init__(self):
        super().__init__(QQuickImageProvider.Image)
        self._source = ""

    @Property(str, notify=sourceChanged)
    def source(self):
        return self._source

    @source.setter
    def source(self, value):
        if self._source != value:
            self._source = value
            self.sourceChanged.emit()       

    def requestImage(self, id, size):
        image = QImage("/home/death916/code/python/deathclock/sacramento_weather_map.png")  # Load the image from a file
        size = image.size()  # Get the size of the image
        return image, size


    
   