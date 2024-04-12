from hx711_spi import HX711
from machine import SPI


class M_HX711(HX711):
    def __init__(self, pd_sck, dout, spi: SPI, gain: int = 128):
        super().__init__(pd_sck, dout, spi, gain)
        self.calibration_offset = 0

    def calibrate(self, n: int = 10) -> None:
        print("Remove any weight from the sensor.\nCalibrating...")
        self.calibration_offset = self.read_average(n)
        print(f"Calibration offset: {self.calibration_offset}")

    def read(self) -> int:
        return super().read()# - self.calibration_offset

    def read_average(self, n: int = 10):
        return super().read_average(n) - self.calibration_offset
