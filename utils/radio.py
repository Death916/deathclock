#!/usr/bin/python3
# connect to rda5807 chip and control it and display the current station
# TODO: reference rd library in readme
import reflex as rx

# from utils.python_rd5807m.radio import Radio as Radio_lib

CURRENT_STATION = "90.9 FM"
PLAYING = False


class Radio(rx.Base):
    def open_radio_button(self):
        return rx.button("Radio", on_click=self.open_radio_button)

    def radio_card(self):
        radio_card = rx.popover.root(
            rx.popover.trigger(rx.button("Radio")),
            rx.popover.content(
                rx.vstack(
                    rx.heading("Current Station"),
                    rx.text(CURRENT_STATION),
                    # rx.text("Volume"),
                    # rx.button("Play"
                    # on_click=Radio_Control.play_radio),
                    # ),
                    # rx.button("Pause"),
                    # rx.button("Stop"),
                ),
            ),
        )
        return radio_card


class Radio_Control:
    def init_radio(self):
        self.radio = Radio_lib()
        self.radio.initialize()

    def play_radio(self):
        pass


## for testing chip
# if __name__ == "__main__":
#   radio = Radio_Control()
#  radio.play_radio()
