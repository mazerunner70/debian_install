from subprocess import Popen, PIPE
from pathlib import Path
import time
import subprocess
from LinuxBlockViewer import LinuxBlockViewer
import sys

class FormatSdCard:

    def validateSdCardReady(self):
        # 1. confirm that the removeable drive is present
        # 2. check if any mounts have already been setup
        # 3. unmount where neecessary
        # 4. return the drive block id
        # Step 1
        blockViewer = LinuxBlockViewer()
        blockDevicesRawText = blockViewer.getLsblkOutputText()
        removeableDriveIds = blockViewer.getRemoveableDriveId(blockDevicesRawText)
        if len(removeableDriveIds) != 1:
            raise RuntimeError('expected 1 removeable drive, found '+removeableDriveIds)
        response = raw_input('Found removeable disc named "'+removeableDriveIds[0]+'". Proceed? [y/N]')
        if response.capitalize() != 'Y':
            print("Exiting...")
            sys.exit(0)
        # Step 2
        mountedBlocks = blockViewer.getBlocksForDriveId(blockDevicesRawText, removeableDriveIds[0])
        if len(mountedBlocks)>0:
            print ('Drive {} has {} blocks mounted. {}'.format(removeableDriveIds[0], len(mountedBlocks), mountedBlocks))
            response = raw_input('These will need to be unmounted. Proceed?[y/N]')
            if response.capitalize() != 'Y':
                print("Exiting...")
                sys.exit(0)
        # Step 3
            for block in mountedBlocks:
                blockViewer.unmountBlock(blockDevicesRawText, block)
        return removeableDriveIds[0]


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
 #       print (progressLineChunks)
        progress = float(progressLineChunks[0])
        print (progress)
        return progress / raspbianImageFileSize

    def executeFormatCommand(self):
        blockDevice = self.validateSdCardReady()
        raspbianImage = self.findRaspbianImage()
        raspbianImageFileSize = raspbianImage.stat().st_size
        print ('Image file size: '+ str(raspbianImageFileSize))
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
    
if __name__ == '__main__':
    cd = FormatSdCard()
    cd.executeFormatCommand()
    
                        
