#!/usr/sbin/setkey -f
## Host 1 script
## Host 1: 192.168.1.31
## Host 2: 192.168.1.32
flush;
spdflush;

add 192.168.1.31 192.168.1.32 ah 1000 -A hmac-md5 "1234567890123456";
add 192.168.1.32 192.168.1.31 ah 2000 -A hmac-md5 "1234567890123456";

add 192.168.1.31 192.168.1.32 esp 1001 -E 3des-cbc "123456789012345678901234" -A hmac-sha1 "12345678901234567890";
add 192.168.1.32 192.168.1.31 esp 2001 -E 3des-cbc "123456789012345678901234" -A hmac-sha1 "12345678901234567890";

spdadd 192.168.1.31 192.168.1.32 any -P out ipsec esp/transport//require ah/transport//require;
spdadd 192.168.1.32 192.168.1.31 any -P in ipsec esp/transport//require ah/transport//require;
