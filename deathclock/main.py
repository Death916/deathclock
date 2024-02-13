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
import weather



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
    # create instance of weather class
    weather_obj = weather.Weather()
    weather_obj.weatherUpdated.connect(lambda weather_map_path: engine.rootContext().setContextProperty("weatherMapPath", weather_map_path))

    # set timer for weather map
    weatherTimer = QTimer()
    weatherTimer.setInterval(300000) # 10 minutes 
    weatherTimer.timeout.connect(weather_obj.download_sacramento_weather_map(engine))
    weather_obj.download_sacramento_weather_map(engine)


    
    
    weatherTimer.start()
    
   
    # create instance of clock class
    timeupdate = clock()
    
    # start timer for clock
    timer = QTimer()
    timer.setInterval(100)  # msecs 100 = 1/10th sec
    timer.timeout.connect(timeupdate.update_time)
    timer.start()
    
    # create instance of news class
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
    