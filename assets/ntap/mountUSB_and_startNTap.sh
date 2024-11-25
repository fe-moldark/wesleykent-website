#!/bin/bash
echo '' > /home/ntap/log.log
echo '> Starting cronjob @reboot...' >> /home/ntap/log.log


while true; do
    echo '+1 wait' >> /home/ntap/log.log
    if [ -b /dev/sda1 ]; then
        sudo mount -t exfat -o uid=1000,gid=1000,dmask=0000,fmask=0000 /dev/sda1 /mnt/usb_dev1 >> /home/ntap/log.log 2>&1
        sudo chown -R ntap:ntap /mnt/usb_dev1/ >> /home/ntap/log.log 2>&1
        break
    fi
    sleep 1
done


sudo /usr/bin/python3 /home/ntap/main.py >> /home/ntap/log.log 2&>1

echo '> Cronjob ended' >> /home/ntap/log.log
