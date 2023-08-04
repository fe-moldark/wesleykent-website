from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time, onewire, ds18x20

SensorPin = Pin(26, Pin.IN)
sensor = ds18x20.DS18X20(onewire.OneWire(SensorPin))
roms = sensor.scan()

i2c=I2C(0,sda=Pin(0), scl=Pin(1), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)
cur_temp='Error'

while True:

    sensor.convert_temp()
    time.sleep(2)
    for rom in roms: #only one here, don't worry
        cur_temp_celsius=round(sensor.read_temp(rom),1)
        cur_temp = int(cur_temp_celsius * 1.8) + 32
        
    oled.fill(0)
    oled.text("Wake up, Neo...", 0, 0)
    oled.text("The Matrix has", 0, 12)
    oled.text("you...", 0, 24)

    oled.text("Also the temp is", 0, 42) #why the hell do they not support the degree symbol??
    oled.text(str(cur_temp)+" F / "+str(int(cur_temp_celsius))+" C", 0, 56) #chr(176) does not work
    
    oled.show()
