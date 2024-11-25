import time, math
from datetime import datetime
import subprocess
from gpiozero import Button
from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import os, sys
import shlex


#GPIO.cleanup()


shutdown_pin = 18
cycle_pin = 16

shutdown_button = Button(shutdown_pin)
cycle_button = Button(cycle_pin)


mode=2 # Runs an initial cycle function that starts everything and resets the mode to '0'
last_press_time = 0
double_press_interval = 6 # Set to 6 due to the sleep function interfering

tcpdump_process=None


def shutdown_check():
    global last_press_time

    current_time = time.time()
    #print(' + Shutdown button pressed once')
    #print(str(current_time), str(last_press_time), str(double_press_interval), str(current_time - last_press_time < double_press_interval))

    if current_time - last_press_time < double_press_interval:
        #print(" ! Double-press detected, shutting down...")
        disp.fill(0)
        disp.show()
        time.sleep(5)
        os.system("sudo shutdown -h now")

    last_press_time = current_time

# Adjust to your filter needs
tcpdump_to_usb="sudo tcpdump -i br0 'not icmp and not arp and not ether broadcast and not ether multicast' -C 1000 -w "

def cycle_function(tcpdump_to_usb):
    global mode
    global tcpdump_process

    #print(" + Button pressed, cycling mode")

    if mode==0: # Changing from default ntap USB to ntap eth2
        mode+=1
        tcpdump_process.terminate()
        os.system("sudo /bin/bash /home/ntap/eth2_mirror.sh")
      
        #print('Changed mode to: ',mode)

    elif mode==1: # Changing from ntap eth2 to 'standard' dhcp on eth0, this also keeps the br0 interface up
        mode+=1

        os.system("sudo rm /etc/network/interfaces")
        os.system("sudo cp /etc/network/interfaces.dhcp /etc/network/interfaces")

        os.system("sudo systemctl restart networking")
        os.system("sudo /bin/bash /home/ntap/adhoc.sh")



    else: # Mode=2 (in dhcp), reload into default ntap usb
        mode=0

        current_time = datetime.now()
        base_name=str(current_time.strftime("%m-%d-%H-%M"))

        n = 0
        while True:
            filename = base_name+"_"+str(n)+".pcap"

            if not os.path.exists('/mnt/usb_dev1/'+str(filename)):
                break
            n += 1

        os.system("sudo rm /etc/network/interfaces")
        os.system("sudo cp /etc/network/interfaces.bridged /etc/network/interfaces")

        os.system("sudo systemctl restart networking")
        os.system("sudo /bin/bash /home/ntap/adhoc.sh")

        time.sleep(1)

        #print(tcpdump_to_usb+'/mnt/usb_dev1/'+str(filename))
        tcpdumpAsList=shlex.split(tcpdump_to_usb+'/mnt/usb_dev1/'+str(filename))

        #os.system(tcpdump_to_usb+'/mnt/usb_dev1/'+str(filename))
        tcpdump_process = subprocess.Popen(tcpdumpAsList)
      

# Run once at start to begin tcpdump on usb stick
cycle_function(tcpdump_to_usb)

shutdown_button.when_pressed = shutdown_check
cycle_button.when_pressed = cycle_function


# OLED stuff here
i2c = busio.I2C(SCL, SDA)
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

disp.fill(0)
disp.show()

width = disp.width
height = disp.height
image = Image.new("1", (width, height))

draw = ImageDraw.Draw(image)

draw.rectangle((0, 0, width, height), outline=0, fill=0)

padding = -2
top = padding
bottom = height - padding
x = 0
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 10)


# Scenario 1: ntap write to usb
#    Mode: NTap USB
#    Storage left:
# Scenario 2: ntap write to eth2
#    Mode: NTap ETH2
#    IP: Link State: UP
# scenario 3: normal operation mode
#    Mode: Default Alter.
#    IP: ip address


switch=0

while True:

    if switch==0:
        switch=1
    else:
        switch=0

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    #print('Mode: ',mode)

    if mode==0: #ntap usb
        line1='> Mode: Ntap USB'
        stat = os.statvfs('/dev/sda1')
        total_size = stat.f_blocks * stat.f_frsize
        used_size = (stat.f_blocks - stat.f_bfree) * stat.f_frsize

        def convert_size(size_bytes):
            if size_bytes == 0:
                return "0B"
            size_name = ("B", "KB", "MB", "GB", "TB")
            i = int(math.floor(math.log(size_bytes, 1024)))
            p = math.pow(1024, i)
            s = round(size_bytes / p, 2)
            return f"{s} {size_name[i]}"

        # Format the sizes in a human-readable way
        total_size_hr = convert_size(total_size)
        used_size_hr = convert_size(used_size)

        cmd="df -h /dev/sda1 | awk 'NR==2 {print $2}'"

        line4='> Usage: '+str(used_size_hr)+' \\ '+str(total_size_hr)

    elif mode==1:
        line1='> Mode: Ntap Eth2'
        if os.path.exists(f"/sys/class/net/eth2"):
            line4='> Eth2 State: Up'
        else:
            line4='> Eth2 State: Down'

    elif mode==2:
        line1='> Mode: Standard'
        cmd = "hostname -I | cut -d' ' -f1"
        IP = subprocess.check_output(cmd, shell=True).decode("utf-8")
        line4='> IP: '+str(IP)

    cpu_cmd = "cut -f 1 -d ' ' /proc/loadavg"
    cpu_usage = float(subprocess.check_output(cpu_cmd, shell=True).decode("utf-8")) * 100
    CPU=f"{cpu_usage:.0f}%"

    mem_cmd = "free -m | awk 'NR==2{printf \"%.2f\", $3*100/$2 }'"
    mem_usage = float(subprocess.check_output(mem_cmd, shell=True).decode("utf-8"))
    MEM=f"{mem_usage:.0f}%"
    line2='> CPU: '+str(CPU)+' \\\\ MEM: '+str(MEM)

    procfile=open('/proc/uptime', 'r')
    uptime_seconds = float(procfile.readline().split()[0])
    uptime_hours = uptime_seconds / 3600
    procfile.close()
    line3='> Uptime: '+f"{uptime_hours:.0f} hr(s)" #str(uptime_hours)

    if switch==0:
        line_2_or_3=line2
    elif switch==1:
        line_2_or_3=line3

    draw.text((x, top + 0), line1, font=font, fill=255)
    draw.text((x, top + 12), line_2_or_3, font=font, fill=255)
    draw.text((x, top + 24), line4, font=font, fill=255)

    # Display image
    disp.image(image)
    disp.show()
    time.sleep(5)
  
