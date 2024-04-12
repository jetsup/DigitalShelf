from machine import SoftSPI, Pin, SoftI2C
from hx711_spi import HX711
from hx711 import M_HX711
from conf import *
from utime import sleep_ms
from lcd_i2c import LCD
import dht
from time import sleep

spi = SoftSPI(
    baudrate=1000000,
    polarity=0,
    phase=0,
    sck=Pin(SPI_SCK_PIN),
    mosi=Pin(SPI_MOSI_PIN),
    miso=Pin(SPI_MISO_PIN),
)
i2c = SoftI2C(scl=Pin(LCD_SCL_PIN), sda=Pin(LCD_SDA_PIN), freq=400_000)

lcd = LCD(I2C_ADDR, LCD_NUM_COLS, LCD_NUM_ROWS, i2c=i2c)

# hx = HX711(Pin(HX711_SCK_PIN), Pin(HX711_OUT_PIN), spi)
hx = M_HX711(Pin(HX711_SCK_PIN), Pin(HX711_OUT_PIN), spi)
dht = dht.DHT11(Pin(DHT_PIN))  # assuming connected to GPIO 26

# hx.OFFSET = 104700#0  # -150000
hx.calibrate()
hx.set_gain(128)
hx.set_offset(104700)
sleep_ms(50)

lcd.begin()
sleep_ms(50)
lcd.cursor_off()
lcd.print("MThorny Store")
sleep(2)

print(hx.read_average(10))
lcd.clear()

prev_val = 0
while True:
    try:
        dht.measure()
        temperature = dht.temperature()
        humidity = dht.humidity()
        lcd.set_cursor(0, 1)
        lcd.print("T: " + str(temperature) + "'C   H:" + str(humidity) + "%")
    except:
        temperature = 0
        humidity = 0
    # reading = 0 if (hx.read_average(5) - 105350) <= 0 else hx.read_average(5) - 105350
    reading = (
        0 if (hx.read_average(5) / 1000) < 200 else (hx.read_average(5) / 1000) - 200
    )
    if reading != prev_val:
        prev_val = reading
        lcd.set_cursor(0, 0)
        print("Weight: " + str(reading))
        # lcd.clear()
        lcd.print("Weight: " + str(reading))
