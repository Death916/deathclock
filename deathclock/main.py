#deathclock
import datetime
import time
import sys
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QTimer, QObject, Signal, Slot
from time import strftime, localtime


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
    def map():

        return

    def cur_weather(): 

        pass

class gui():
     def handleTouchAreaPressed(self, signal):
        # Implement your desired behavior when the left area is pressed
        print("here touch area")
        leftTouchAreaMouse = engine.rootObjects()[0].findChild("leftTouchAreaMouse")
        leftTouchAreaMouse.connect(b"touchAreaPressed", self.handleTouchAreaPressed)
        print("Left area pressed!")

def main():
    gui_obj = gui()
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