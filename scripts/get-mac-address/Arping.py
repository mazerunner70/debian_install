from subprocess import Popen, PIPE

class Arping:

    def execute(self, ipAddress):
        process = Popen(["arping", "-fI","enp0s8",ipAddress], stdout=PIPE,stderr=PIPE)
        response = process.communicate()
        error = response[1]
        if len(error) > 0:
            print (error)
            raise RuntimeError("error running arping")
        stdout = response[0].decode("utf-8").split("\n")
        return stdout[1]

    def getMacAddress(self, line):
        return line.split(' ')[4].strip('[]')

    

if __name__ == '__main__':
    from ReadNmap import ReadNmap
    readNmap = ReadNmap()
    ip = readNmap.findIpOfHost('raspberrypi')
    arping = Arping()
    line = arping.execute(ip)
    print (arping.getMacAddress(line))