from machine import SoftSPI, Pin, SoftI2C
from hx711_spi import HX711
from conf import *
from utime import sleep_ms
from lcd_i2c import LCD

spi = SoftSPI(
    baudrate=1000000,
    polarity=0,
    phase=0,
    sck=Pin(SPI_SCK_PIN),
    mosi=Pin(SPI_MOSI_PIN),
    miso=Pin(SPI_MISO_PIN),
)
i2c=SoftI2C(scl=Pin(LCD_SCL_PIN), sda=Pin(LCD_SDA_PIN), freq=400_000)

lcd = LCD(I2C_ADDR, LCD_NUM_COLS, LCD_NUM_ROWS, i2c=i2c)

hx = HX711(Pin(HX711_SCK_PIN), Pin(HX711_OUT_PIN), spi)

# hx.OFFSET = 104700#0  # -150000
hx.set_gain(128)
hx.set_offset(104700)
sleep_ms(50)

lcd.begin()
sleep_ms(50)
lcd.cursor_off()
lcd.print("Hello, world!")


print(hx.read_average(10))
lcd.clear()
while True:
    reading = hx.read_average(5) - 104950
    print(reading)
    lcd.clear()
    lcd.print(str(reading))
