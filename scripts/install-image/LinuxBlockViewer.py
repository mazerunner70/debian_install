from subprocess import Popen, PIPE
from pathlib import Path
import time
import subprocess
import re

class LinuxBlockViewer:
    blockNameRegexPattern = re.compile('NAME=\\"(.*?)\\"')
    mountpointRegexPattern = re.compile('MOUNTPOINT=\\"(.*?)\\"')
    def makeLinuxCall(self, commandList, cmdDescription):
        process = Popen(commandList, stdout=PIPE,stderr=PIPE)
        response = process.communicate()
        error = response[1]
        if len(error) > 0:
            raise RuntimeError("error when "+str(cmdDescription))
        stdout = response[0].decode("utf-8").split("\n")
        return stdout[:-1]

    def getLsblkOutputText(self):
        return self.makeLinuxCall(["lsblk", "-Po","name,rm,subsystems,mountpoint"], 'checking block devices for removable drive')

    def getRemoveableBlockIdText(self, lsblkOutputText):       
        return [LinuxBlockViewer.blockNameRegexPattern.search(x).group(1) for x in lsblkOutputText if x.find('RM="1"') != -1]

    def getFullBlockList(self, lsblkOutputText):
#        print(lsblkOutputText)
        return [LinuxBlockViewer.blockNameRegexPattern.search(x).group(1) for x in lsblkOutputText]

    def getRemoveableDriveId(self, lsblkOutputText):
        removeableBlockIdList = self.getRemoveableBlockIdText(lsblkOutputText)
        return [x for x in removeableBlockIdList if len(x) == 3]

    def getBlocksForDriveId(self, lsblkOutputText, driveId):
        fullBlockList = self.getFullBlockList(lsblkOutputText)
        return [x for x in fullBlockList if x.startswith(driveId) and len(x) == 4]

    def getMountpointForBlock(self, lsblkOutputText, blockId):
        name = 'NAME="'+blockId+'"'
#        print (name)
#        print (lsblkOutputText)
#        print (lsblkOutputText[0].find(name))
#        print (lsblkOutputText[1].find(name))
#        print (lsblkOutputText[1])
        return [LinuxBlockViewer.mountpointRegexPattern.search(x).group(1) for x in lsblkOutputText if x.find(name) != -1]

    def unmountBlock(self, lsblkOutputText, blockId):
        mountPoints = self.getMountpointForBlock(lsblkOutputText, blockId)
        if len(mountPoints) != 1:
            raise RuntimeError('Confused, blockId'+blockId+' did not have a single mountpoint: '+mountPoint)
        mountPoint = mountPoints[0]
        if len(mountPoint) == 0:
            print('Ignoring block '+blockId+', no mount found')
        else:
            print('Unmounting '+blockId+'...')
            self.makeLinuxCall(['sudo', 'umount',mountPoint], 'unmounting '+blockId)
            print('unmounted '+blockId)





    
                        
