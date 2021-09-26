#deathclock
import time
import dearpygui.dearpygui as dpg


class clock():

    def time_and_date(self):
        print(time.asctime())

    def alarm(self):
        alarm_time = None

        def ring():
            pass


class weather():
    def map(self):
        return

    def cur_weather(self):
        pass


class gui():
    def show_time(self):

        with dpg.window(label="time"):
            dpg.add_text(time.asctime())
            dpg.start_dearpygui()


def main():
    gui1 = gui()
    gui1.show_time()


    
if __name__ == "__main__":
    main()


