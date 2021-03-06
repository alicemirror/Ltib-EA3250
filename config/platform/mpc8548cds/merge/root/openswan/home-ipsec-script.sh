#!/bin/sh
ifconfig eth0 down
ifconfig eth0 hw ether 00:e0:0c:02:00:fd
ifconfig eth0 -arp
ifconfig eth0 192.168.3.160
ifconfig eth0 up
ifconfig eth1 down
ifconfig eth1 hw ether 00:E0:0C:00:01:FB
ifconfig eth1 200.200.200.10
ifconfig eth1 up
sleep 1
arp -s 192.168.3.21 00:00:00:00:00:01
arp -s 200.200.200.20 04:00:00:00:00:0B
echo "1" > /proc/sys/net/ipv4/ip_forward
route add default dev eth1
ipsec setup --start



