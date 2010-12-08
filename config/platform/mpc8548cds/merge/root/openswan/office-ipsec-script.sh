#!/bin/sh
ifconfig eth0 down
ifconfig eth0 hw ether 00:e0:0c:00:00:fd
ifconfig eth0 -arp
ifconfig eth0 192.168.2.160
ifconfig eth0 up
ifconfig eth1 down
ifconfig eth1 hw ether 04:00:00:00:00:0B
ifconfig eth1 200.200.200.20
ifconfig eth1 up
sleep 1
arp -s 192.168.2.21 00:00:00:00:00:02
arp -s 200.200.200.10 00:E0:0C:00:01:FB
echo "1" > /proc/sys/net/ipv4/ip_forward
route add default dev eth1
ipsec setup --start


