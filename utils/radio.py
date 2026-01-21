import logging
import time

# Try to import the hardware library, fall back to dummy if fails
try:
    from utils.python_rd5807m.radio import Radio as RadioLib
    HARDWARE_AVAILABLE = True
except ImportError:
    HARDWARE_AVAILABLE = False


class DummyDevice:
    def __init__(self):
        self.volume = 5
        self.freq = 90.9
        self.muted = False
        self.stereo = True
        self.bass = False

    def on(self):
        logging.info("DummyRadio: Powered ON")

    def off(self):
        logging.info("DummyRadio: Powered OFF")

    def set_volume(self, value):
        self.volume = value
        logging.info(f"DummyRadio: Set volume to {value}")

    def set_frequency(self, frequency):
        self.freq = frequency
        logging.info(f"DummyRadio: Set frequency to {frequency}")

    def set_mute(self, value):
        self.muted = value
        logging.info(f"DummyRadio: Mute {value}")

    def set_stereo(self, value):
        self.stereo = value
        logging.info(f"DummyRadio: Stereo {value}")

    def set_bass(self, value):
        self.bass = value
        logging.info(f"DummyRadio: Bass {value}")

    def close(self):
        logging.info("DummyRadio: Closed")


class Radio:
    def __init__(self):
        self.device = None
        self.is_on = False
        self.volume = 5
        self.station = 90.9
        self._initialize_device()

    def _initialize_device(self):
        if HARDWARE_AVAILABLE:
            try:
                self.radio_lib = RadioLib()
                self.radio_lib.initialize()
                self.device = self.radio_lib.device
                logging.info("Radio: Hardware device initialized successfully.")
            except Exception as e:
                logging.error(f"Radio: Hardware init failed ({e}). Using Dummy.")
                self.device = DummyDevice()
        else:
            logging.info("Radio: Hardware lib not found. Using Dummy.")
            self.device = DummyDevice()

    def on(self):
        if self.device:
            self.device.on()
            self.is_on = True

    def off(self):
        if self.device:
            self.device.off()
            self.is_on = False

    def set_volume(self, volume: int):
        """Set volume 0-15"""
        if self.device:
            # Ensure volume is within bounds if needed, though UI likely handles it
            vol = max(0, min(15, int(volume)))
            self.device.set_volume(vol)
            self.volume = vol

    def set_station(self, station: float):
        if self.device:
            self.device.set_frequency(float(station))
            self.station = station

    def get_info(self):
        """Return current state as dict"""
        return {
            "is_on": self.is_on,
            "volume": self.volume,
            "station": self.station,
        }
