# Termometer and hygrometer with HTU21D sensor and oled display
# requires micropython-ssd1306 library
# Pepp_diy 2021

import machine, time
from machine import Pin
from ssd1306 import SSD1306_I2C
import framebuf

led = Pin(25, Pin.OUT)      # onboard led

WIDTH  = 128                # oled display width
HEIGHT = 64                 # oled display height

sda=machine.Pin(8)          # i2c interface pins
scl=machine.Pin(9)
i2c=machine.I2C(0,sda=sda, scl=scl, freq=400000)
    
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)              # Init oled display    

# Read UHT21D 
def read_htu21d(ad):
    val = bytearray(1)
    val[0] = ad
    i2c.writeto(0x40, val, False)     # 0x40 htu21d i2c address
    time.sleep(0.1)                   # wait for conversion
    bytes = i2c.readfrom(0x40, 2)
    r = (bytes[1] & 252) + (bytes[0] * 256)
    return r

while True:
    led.high()                         # turn on onboard led
    v = read_htu21d(0xF3)              # 0xF3 read temperature
    t = v * 175.72 / 65536;
    t -= 46.85
    v = read_htu21d(0xF5)              # 0xF5 read humidity
    h = v * 125 / 65536;
    h -= 6;

    print ('Temperature %.2f °C' %t) 
    print ('Humidity %.1f' %h)
    tt = "T %.2f" % t                # convert values in string
    hh = "RH %.1f" % h
    oled.fill(0)
    oled.text(tt,5,30)
    oled.text(hh,5,40)  
    oled.show()    
    led.low()                        # turn off onboard led
    time.sleep(2)                    # 2 seconds delay
