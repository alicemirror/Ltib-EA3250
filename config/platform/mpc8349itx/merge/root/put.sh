#!/bin/sh
busybox tftp -p -l $1 -r $tftp_path/$1 $serverip
