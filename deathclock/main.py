#deathclock
import datetime
import time
import sys
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QTimer, QObject, Signal, Slot, Property
from time import strftime, localtime
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os
import news


class clock():
    def update_time(self):
        curr_time = strftime("%B %d, %I:%M %p", localtime())
        
        engine.rootObjects()[0].setProperty('currTime', curr_time)
        
        
        return curr_time
        
       
    def time_and_date():
        print(time.asctime())
    
    def alarm():
        alarm_time =  input("what time should the alarm be set?")


        def ring():
            pass


class weather():
    
    def __init__(self, image_provider):
        self.image_provider = image_provider
        #save radar map from google weather
    
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
        os.remove(file)
        print("old screen shot deleted")


class WeatherImageProvider(QObject):
    """weather image provider class to provide image to qml when timer is up"""
    sourceChanged = Signal()
    

    def __init__(self):
        super().__init__()
        self._source = ""

    @Property(str, notify=sourceChanged)
    def source(self):
        return self._source

    @source.setter
    def source(self, value):
        if self._source != value:
            self._source = value
            self.sourceChanged.emit()       

                                
"""
class gui():
     def handleTouchAreaPressed(self, signal):
        # Implement your desired behavior when the left area is pressed
        print("here touch area")
        leftTouchAreaMouse = engine.rootObjects()[0].findChild("leftTouchAreaMouse")
        leftTouchAreaMouse.connect(b"touchAreaPressed", self.handleTouchAreaPressed)
        print("Left area pressed!")
"""
def main():
    #gui_obj = gui()
    
    app = QGuiApplication(sys.argv)
    global engine
    engine = QQmlApplicationEngine()
    engine.quit.connect(app.quit)
    
    engine.load( 'main.qml')
    # create instance of  weather image provider
    image_provider = WeatherImageProvider()

    # set context property for weather image provider
    context = engine.rootContext()
    context.setContextProperty("imageProvider", image_provider)

    # create instance of weather class
    weather_obj = weather(image_provider)
    weather_obj.download_sacramento_weather_map()

    # create instance of clock class
    timeupdate = clock()
    timer = QTimer()
    weatherTimer = QTimer()
    weatherTimer.start()
    # set timer for weather map
    weatherTimer.setInterval(600000) # 10 minutes 
    weatherTimer.timeout.connect(weather_obj.download_sacramento_weather_map)
    timer.setInterval(100)  # msecs 100 = 1/10th sec
    timer.timeout.connect(timeupdate.update_time)
    weather_obj.delete_old_screen_shot()

    timer.start()
    news_obj = news.news()
    news_ticker = news_obj.get_news()
    #print(news_obj._news_dict)
    print(news_ticker)
    news_context = engine.rootContext()
    news_context.setContextProperty("news", str(news_ticker))
    #start timer for news
    news_timer = QTimer()
    news_timer.timeout.connect(news_obj.get_news)
    news_timer.setInterval(600000) # 10 minutes

    news_timer.start()
    
    
    sys.exit(app.exec_())



if __name__ == "__main__":
    main()

#TODO: add weather to qml
#TODO: move weather to own file
    