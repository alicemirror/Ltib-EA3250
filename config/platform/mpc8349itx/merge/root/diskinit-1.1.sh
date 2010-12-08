if [ "x$1" == x -o "x$tftp_path" == x -o "x$serverip" == x ]
then
echo "Please define parameter1, tftp_path and serverip."
echo "Currently:"
echo "parameter1=$1"
echo "tftp_path=$tftp_path"
echo "serverip=$serverip"
else
set -o verbose
mke2fs /dev/$1
mkdir -p /mnt/hdd0
mount -t ext2 /dev/$1 /mnt/hdd0
mkdir /mnt/hdd0/boot; cd /mnt/hdd0/boot
echo "TFTPing ext2 image from $serverip:$tftp_path/rootfs.ext2.gz.uboot ..."
busybox tftp -g -l rootfs.ext2.gz.uboot -r $tftp_path/rootfs.ext2.gz.uboot $serverip
dd if=rootfs.ext2.gz.uboot of=rootfs.ext2.gz bs=64 skip=1
rm rootfs.ext2.gz.uboot
gunzip -c rootfs.ext2.gz > rootfs.ext2
mkdir tmpmnt; mount -t ext2 -o loop rootfs.ext2 tmpmnt
cp -a ./tmpmnt/* /mnt/hdd0
umount tmpmnt
cat > /mnt/hdd0/etc/fstab <<EOF
# file system   mount       type    options           dump    pass
/dev/$1       /           ext2    rw,noauto         0       1
proc            /proc       proc    defaults          0       0
devpts          /dev/pts    devpts  gid=5,mode=620    0       0
sysfs           /sys        sysfs   defaults          0       0
EOF
sync
set +o verbose
fi
