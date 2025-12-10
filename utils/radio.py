#!/usr/bin/python3
# connect to rda5807 chip and control it and display the current station

import reflex as rx

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
    def __init__(self):
        pass

    def play_radio(self):
        pass
