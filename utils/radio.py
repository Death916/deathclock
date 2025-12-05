#!/usr/bin/python3
# connect to rda5807 chip and control it and display the current station

import reflex as rx


class Radio(rx.Base):
    def open_radio_button(self):
        return rx.button("Radio", on_click=self.open_radio_button)

    def radio_card(self):
        return rx.card(title="Radio")


class Radio_Control:
    def __init__(self):
        pass
