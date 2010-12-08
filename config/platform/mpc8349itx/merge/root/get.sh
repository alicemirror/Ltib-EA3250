#!/bin/sh
busybox tftp -g -l $1 -r $tftp_path/$1 $serverip
