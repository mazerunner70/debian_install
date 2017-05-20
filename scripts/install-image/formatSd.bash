#!/bin/bash

/usr/bin/python FormatSd.py

echo last command ended with a "$?"
if [[ "$?" -eq "1" ]]; then
	echo "exiting..."
	exit 1 
fi
sudo sync
mkdir -p /home/vagrant/sdb1
sudo mount /dev/sdb1 /home/vagrant/sdb1
sudo touch /home/vagrant/sdb1/ssh
ls -l /home/vagrant/sdb1
sudo umount /home/vagrant/sdb1
sudo sync