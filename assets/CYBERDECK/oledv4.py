import time, math
import board
import busio
from PIL import Image, ImageDraw, ImageFont
from adafruit_ssd1306 import SSD1306_I2C
import psutil
import sys
import socket
import subprocess
import re


def justTurningOffDisplay():
    i2c = busio.I2C(board.SCL, board.SDA)
    display = SSD1306_I2C(128, 32, i2c)

    display.fill(0)
    print('Turning off now')
    display.show()
    time.sleep(2)

    display.fill(0)
    display.show()
    display = None
    sys.exit()


if len(sys.argv)>=2:
    if str(sys.argv[1]).lower()=='off':
        justTurningOffDisplay()
    else:
        pass


i2c = busio.I2C(board.SCL, board.SDA)
oled = SSD1306_I2C(128, 32, i2c)

image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)


font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
font_size = 9
font = ImageFont.truetype(font_path, font_size)

psutil.cpu_percent()


def get_ip_address(interface):
    try:
        result = subprocess.run(["/usr/sbin/ifconfig", interface], capture_output=True, text=True) #must define full path when run from the crontab
        ip_match = re.search(r"inet (\d+\.\d+\.\d+\.\d+)", result.stdout)
        if ip_match:
            return ip_match.group(1)
        else:
            return None
    except subprocess.CalledProcessError:
        return None


def returnOne():
    eth0=get_ip_address('eth0')
    wlan0=get_ip_address('wlan0')

    if eth0==None:
        if wlan0==None:
            return '--No Network--'
        else:
            return 'IP: '+str(wlan0)+' (E)'
    else:
        return 'IP: '+str(eth0)+' (W)'


while True:

    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
    cpu_usage = psutil.cpu_percent() #interval=1)
    memory_usage = psutil.virtual_memory().percent
 
    draw.text((0, 0), returnOne(), font=font, fill=255)
    draw.text((0, 10), f"CPU: {cpu_usage:.1f}%", font=font, fill=255)
    draw.text((0, 21), f"MEM: {memory_usage:.1f}%", font=font, fill=255)
    
    oled.image(image)
    oled.show()

    time.sleep(5)
