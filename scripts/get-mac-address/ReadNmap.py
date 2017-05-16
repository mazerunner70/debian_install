from subprocess import Popen, PIPE
import re, sys

class ReadNmap:

    def executeNetworkRead(self):
        process = Popen(["nmap", "-sL","192.168.0.0/24"], stdout=PIPE,stderr=PIPE)
        response = process.communicate()
        error = response[1]
        if len(error) > 0:
            raise RuntimeError("error running nmap")
            print (error)
        stdout = response[0].decode("utf-8").split("\n")
        return stdout[:-1]

    def filterOutEmptyIp(self, rawNmapOutput):
        filteredList = []
        #iterate across raw list
        for line in rawNmapOutput:
            if line.find('(192')!= -1:
                filteredList.append(line)
        return filteredList

    def mapNameToIp(delf, filteredNmapEntries):
        map = {}
        for line in filteredNmapEntries:
            strings = line.split(' ')
#            print (strings[4], strings[5])
            map[strings[4]] = strings[5].strip('()')
        return map

    def findIpOfHost(self, hostname):
        namesMap = self.executeNmap()
        return namesMap[hostname]
        

    def executeNmap(self):
        rawOutput = self.executeNetworkRead()
        filteredOutput = self.filterOutEmptyIp(rawOutput)
        mapIds = self.mapNameToIp(filteredOutput)
        return mapIds
        



if __name__ == '__main__':
    try:
      readNmap = ReadNmap()
      ip = readNmap.findIpOfHost('raspberrypi')
      print (ip)
    except BaseException as e:
      sys.stderr.write (str(e))
      sys.exit(1)

