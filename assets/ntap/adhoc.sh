#!/bin/bash
sudo ip link set wlan0 down
sudo iw wlan0 set type ibss
sudo ip link set wlan0 up
sudo iw wlan0 ibss join ntap_adhoc 2437
sudo ip addr add 169.254.1.1/16 dev wlan0
sudo systemctl restart dnsmasq
sudo systemctl restart hostapd
