#deathclock
import datetime
import time
import sys
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QTimer, QObject, Signal, Slot
from time import strftime, localtime
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service






class clock():
    def update_time(self):
        curr_time = strftime("%B %d, %I:%M %p", localtime())
        
        engine.rootObjects()[0].setProperty('currTime', curr_time)
        
        
        return curr_time
        # TODO: ADD date 
       
    def time_and_date():
        print(time.asctime())
    
    def alarm():
        alarm_time =  input("what time should the alarm be set?")


        def ring():
            pass


            



class weather():
    
        #save radar map from https://radar.weather.gov/?settings=v1_eyJhZ2VuZGEiOnsiaWQiOiJ3ZWF0aGVyIiwiY2VudGVyIjpbLTExOS44NzYsMzcuNjcxXSwibG9jYXRpb24iOlstMTIwLjY2NiwzNy4wNDRdLCJ6b29tIjo3LjU0ODYxNTg5NDY1NTIyN30sImFuaW1hdGluZyI6ZmFsc2UsImJhc2UiOiJzdGFuZGFyZCIsImFydGNjIjpmYWxzZSwiY291bnR5IjpmYWxzZSwiY3dhIjpmYWxzZSwicmZjIjpmYWxzZSwic3RhdGUiOmZhbHNlLCJtZW51Ijp0cnVlLCJzaG9ydEZ1c2VkT25seSI6ZmFsc2UsIm9wYWNpdHkiOnsiYWxlcnRzIjowLjgsImxvY2FsIjowLjYsImxvY2FsU3RhdGlvbnMiOjAuOCwibmF0aW9uYWwiOjAuNn19
    @staticmethod
    

    def download_sacramento_weather_map():
        url = "https://www.google.com/search?q=weather&hl=en-GB"
        service = Service(executable_path='/home/death916/code/python/deathclock/deathclock/chromedriver')
        options = webdriver.ChromeOptions()
        #options.add_argument('--headless')
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)
        map_element = driver.find_element('id', 'wob_wc')
        map_element.screenshot('sacramento_weather_map.png')
        driver.quit()

        def cur_weather():
            # scrape weather from web
            

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
    weather_obj = weather()
    #weather_obj.download_sacramento_weather_map()
    app = QGuiApplication(sys.argv)
    global engine
    engine = QQmlApplicationEngine()
    engine.quit.connect(app.quit)
    engine.load( 'main.qml')
    timeupdate = clock()
    timer = QTimer()
    timer.setInterval(100)  # msecs 100 = 1/10th sec
    timer.timeout.connect(timeupdate.update_time)
    
    
   
    timer.start()
  

    
    
    sys.exit(app.exec_())



if __name__ == "__main__":
    main()