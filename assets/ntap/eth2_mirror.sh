#!/bin/bash
sudo ip link set eth2 down
sudo ip link set eth2 promisc on
sudo ip link set eth2 up

sudo tc qdisc del dev br0 ingress
sudo tc qdisc add dev br0 handle ffff: ingress

sudo tc filter add dev br0 parent ffff: protocol all u32 match u32 0 0 action mirred egress mirror dev eth2
