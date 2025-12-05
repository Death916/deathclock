#!/usr/bin/python3
# connect to rda5807 chip and control it and display the current station

import reflex as rx


class Radio(rx.Base):
    def open_radio_button(self):
        return rx.button("Radio", on_click=self.open_radio_button)

    def radio_card(self):
        radio_card = rx.card(
            rx.vstack(
                rx.heading("Radio"),
                rx.text("Current Station"),
                #  rx.text("Volume"),
                # rx.button("Play"),
                # rx.button("Pause"),
                # rx.button("Stop"),
            ),
        )
        return radio_card


class Radio_Control:
    def __init__(self):
        pass
