#!/bin/bash

/usr/bin/python3.5 <<END
from FormatSd import FormatSdCard
cd = FormatSdCard()
cd.executeFormatCommand()
END
sudo sync
mkdir -p /home/vagrant/sdb1
sudo mount /dev/sdb1 /home/vagrant/sdb1
sudo touch /home/vagrant/sdb1/ssh
ls -l /home/vagrant/sdb1
sudo umount /home/vagrant/sdb1
sudo sync