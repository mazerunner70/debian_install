from subprocess import Popen, PIPE
from pathlib import Path
import time
import subprocess

class FormatSdCard:

    def listBlockDevices(self):
        process = Popen(["lsblk", "-dPo","name,rm"], stdout=PIPE,stderr=PIPE)
        response = process.communicate()
        error = response[1]
        if len(error) > 0:
            raise RuntimeError("error checking block devices")
        stdout = response[0].decode("utf-8").split("\n")
        return stdout[:-1]

    def findRemoveableBlockDevice(self):
        blockDevices = self.listBlockDevices()
        removeableBlockDevice = ""
        for blockDevice in blockDevices:
            if blockDevice.find('RM="1"') != -1 and removeableBlockDevice == "" :
                removeableBlockDevice = blockDevice[6:9]
        print( "Block found to write to:", removeableBlockDevice)
        if len(removeableBlockDevice) != 3:
            raise RuntimeError("Expected 3 letter id for block")
        return removeableBlockDevice

    def findRaspbianImage(self):
        vagrantShare = Path('/vagrant')
        if not vagrantShare.exists():
            raise RuntimeError("vagrant share folder not present")
        if not vagrantShare.is_dir():
            raise RuntimeError("vagrant share folder not a directory")
        imageDir = vagrantShare / 'images/raspbian'
        if not imageDir.exists():
            raise RuntimeError("Raspbian image share folder not present '{}'".format( imageDir ))
        if not imageDir.is_dir():
            raise RuntimeError("Raspbian image share folder not a directory")
        files = sorted(imageDir.glob('*'))
        print (files)
        if len(files) != 1 :
            raise RuntimeError("Expected only one file in the image dir, found " + str(len(files)))
        imageFile = files[0]
        if not imageFile.is_file():
            raise RuntimeError("Raspbian image share folder not a directory")
        return imageFile

    def calculateProgress(self, line, raspbianImageFileSize):
#        print ("line:", line)
        progressLineChunks = line.split(' ')
#        print (progressLineChunks)
        progress = int(progressLineChunks[0])
        return progress / raspbianImageFileSize

    def executeFormatCommand(self):
        blockDevice = self.findRemoveableBlockDevice()
        raspbianImage = self.findRaspbianImage()
        raspbianImageFileSize = raspbianImage.stat().st_size
        print ('Executing command "dd bs=4M if={} of=/dev/{}"'.format(raspbianImage, blockDevice))
        process = Popen(["sudo",
                         "dd",
                         "bs=4M",
                         "if={}".format(raspbianImage),
                         "of=/dev/{}".format(blockDevice)], stdout=PIPE,stderr=PIPE, universal_newlines=True, bufsize=1)
        while process.poll() is None:
#            print ('l')
            subprocess.call(['sudo','pkill','-USR1','-n','-x','dd'])
#            print ('m')
            line = ''
            for count in range(3):
                line = process.stderr.readline()
#                print('=',line)
            progress = self.calculateProgress(line, raspbianImageFileSize)
            print ('Progress: {:.1%}'.format(progress))
            time.sleep(10)
        print ("Imaging completed successfully")
    

    
                        
