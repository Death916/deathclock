import logging

import reflex as rx

# from utils.python_rd5807m.radio import Rda5807m as Radio_lib

DEBUG = True
CURRENT_STATION = 90.9
PLAYING = False
HARDWARE = True


class Radio_UI:
    def __init__(self):
        if DEBUG:
            self.device = None
        else:
            self.device = Radio_Control()

    def open_radio_button(self):
        return rx.button("Radio", on_click=self.open_radio_button)

    def radio_card(self):
        """
        Radio Card
        Main pop open button for radio control
        """

        return rx.popover.root(
            rx.popover.trigger(rx.button("Radio")),
            rx.popover.content(
                rx.vstack(
                    rx.heading("Current Station"),
                    rx.text(CURRENT_STATION),
                    # rx.text("Volume"),
                    # rx.button("Play", on_click=self.device.play_radio),
                ),
                # rx.button("Pause"),
                # rx.button("Stop"),
            ),
        )


class Radio_Control:
    """
    Radio Control Class
    uses rda5807m library, if debugging populates false values for display
    """

    def __init__(self):
        self.debug = DEBUG
        self.bus = 1
        self.poll_interval = 0.5
        self.current_station = CURRENT_STATION
        self.volume = 7
        self.playing = False
        self.signal = 0.0
        self._display = None
        self._device = None

    def init_radio(self):
        # self._device = Radio_lib(self.bus)
        # self._device.init_chip()
        pass

    def play_radio(self):
        if self.debug:
            logging.debug("Playing fake radio")
            self._display = rx.text("Playing")
            self.playing = True
        else:
            if self._device:
                self._device.on()
            self.playing = True

    def stop_radio(self):
        if self.debug:
            logging.debug("Stopping radio")
            self._display = rx.text("Stopped")
            self.playing = False
        else:
            if self._device:
                self._device.off()
            self.playing = False

    def set_volume(self, volume):
        if self.debug:
            logging.debug(f"Setting volume to {volume}")
            self.volume = volume
        else:
            if self._device:
                self._device.set_volume(volume)
            self.volume = volume

    def set_station(self, station):
        if self.debug:
            logging.debug(f"Setting station to {station}")
            self.current_station = station
        else:
            self.current_station = station
            logging.info(f"Station set to {station}")

    def station_change_up(self):
        if self.debug:
            pass
        else:
            self.current_station += 0.1

    def station_change_down(self):
        if self.debug:
            pass
        else:
            self.current_station -= 0.1
