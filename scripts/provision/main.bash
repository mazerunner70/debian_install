#!/bin/bash

echo "Provisioning house Wiki"



















echo "1. Format of SD card"
echo "2. Configure Raspberry PI"
echo ""
read -e option

if [ $option -eq 1 ]
then

  echo "Please ensure the SD card is mounted, then hit enter"

 

  echo "Writing image to SD card"
  presentWorkingDirectory=`pwd` 
  cd install-image
  ./formatSd.bash
  cd $presentWorkingDirectory

fi

if [ $option -eq 2 ] || [ $option -eq 1 ]
then
  
  echo "Place SD card in Raspberry PI and start it up on an ethernet connection. Please then hit enter"

  read -e dummy

  cd get-mac-address
  ip_address=`/usr/bin/python3.5 ReadNmap.py`
  echo Raspberry Pi found at IP $ip_address

  mac_address=`/usr/bin/python3.5 Arping.py`
  echo Raspberry Pi mac address of ethernet is $mac_address

  new_ip=`/usr/bin/python3.5 Properties.py $mac_address`
  echo Raspberry Pi will have IP $new_ip
  
  new_hostname=`/usr/bin/python3.5 Properties.py $new_ip`
  echo Raspberry Pi will have hostname $new_hostnam
  
  cd ..

  cd set-static-ip
  ansible-playbook set-static-ip.yml -i inventory -e currentip=$ip_address -e newip=$new_ip -e newhostname=$new_hostname
  cd ..
  
  
fi  


