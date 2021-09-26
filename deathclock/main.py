#deathclock
import time
import dearpygui.dearpygui as dpg


class clock():

    def time_and_date(self):
        return time.asctime()


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
        clock1 = clock()
        timenow = clock1.time_and_date()
        with dpg.window(label="time"):
            dpg.add_text(timenow)


    def show_cur_weather(self):
        with dpg.window(label="Current Weather"):
            dpg.load_image()

    def alarm_button(self):
        with dpg.window(label="Set Alarm"):
            dpg.add_date_picker(track_offset=.5, indent=6)


def main():
    gui1 = gui()
    gui1.show_time()
    gui1.alarm_button()
    dpg.start_dearpygui()



if __name__ == "__main__":
    main()


