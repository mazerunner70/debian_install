import unittest
from LinuxBlockViewer import LinuxBlockViewer

class TestLinuxBlockViewer(unittest.TestCase):

    textNoRemoveableBlock = ('NAME="sda" RM="0" SUBSYSTEMS="block:scsi:pci" MOUNTPOINT=""',
'NAME="sda1" RM="0" SUBSYSTEMS="block:scsi:pci" MOUNTPOINT="/boot"',
'NAME="sda2" RM="0" SUBSYSTEMS="block:scsi:pci" MOUNTPOINT=""',
'NAME="sda5" RM="0" SUBSYSTEMS="block:scsi:pci" MOUNTPOINT=""',
'NAME="vagrant--vg-root" RM="0" SUBSYSTEMS="block" MOUNTPOINT="/"',
'NAME="vagrant--vg-swap_1" RM="0" SUBSYSTEMS="block" MOUNTPOINT="[SWAP]"')
    textRemoveableBlock = ('NAME="sda" RM="0" SUBSYSTEMS="block:scsi:pci" MOUNTPOINT=""',
'NAME="sda1" RM="0" SUBSYSTEMS="block:scsi:pci" MOUNTPOINT="/boot"',
'NAME="sda2" RM="0" SUBSYSTEMS="block:scsi:pci" MOUNTPOINT=""',
'NAME="sda5" RM="0" SUBSYSTEMS="block:scsi:pci" MOUNTPOINT=""',
'NAME="vagrant--vg-root" RM="0" SUBSYSTEMS="block" MOUNTPOINT="/"',
'NAME="vagrant--vg-swap_1" RM="0" SUBSYSTEMS="block" MOUNTPOINT="[SWAP]"',
'NAME="sdb" RM="1" SUBSYSTEMS="block:scsi:usb:pci" MOUNTPOINT=""',
'NAME="sdb1" RM="1" SUBSYSTEMS="block:scsi:usb:pci" MOUNTPOINT="/media/vagrant/boot"',
'NAME="sdb2" RM="1" SUBSYSTEMS="block:scsi:usb:pci" MOUNTPOINT=""')
    test2 = [u'NAME="sda" RM="0" SUBSYSTEMS="block:scsi:pci" MOUNTPOINT=""', u'NAME="sda1" RM="0" SUBSYSTEMS="block:scsi:pci" MOUNTPOINT="/boot"', u'NAME="sda2" RM="0" SUBSYSTEMS="block:scsi:pci" MOUNTPOINT=""', u'NAME="sda5" RM="0" SUBSYSTEMS="block:scsi:pci" MOUNTPOINT=""', u'NAME="vagrant--vg-root" RM="0" SUBSYSTEMS="block" MOUNTPOINT="/"', u'NAME="vagrant--vg-swap_1" RM="0" SUBSYSTEMS="block" MOUNTPOINT="[SWAP]"', u'NAME="sdb" RM="1" SUBSYSTEMS="block:scsi:usb:pci" MOUNTPOINT=""', u'NAME="sdb1" RM="1" SUBSYSTEMS="block:scsi:usb:pci" MOUNTPOINT=""', u'NAME="sdb2" RM="1" SUBSYSTEMS="block:scsi:usb:pci" MOUNTPOINT=""']

    def testRegex(self):
        regex = LinuxBlockViewer.blockNameRegexPattern
        matchObject = regex.search('NAME="sda" RM="0"')
        self.assertTrue(matchObject)
        self.assertEqual(matchObject.group(1), 'sda')
        matchObject = regex.search('NAME="sda1" RM="0"')
        self.assertEqual(matchObject.group(1), 'sda1')
        regex = LinuxBlockViewer.mountpointRegexPattern
        matchObject = regex.search('NAME="sda1" RM="0" SUBSYSTEMS="block:scsi:pci" MOUNTPOINT="/boot"')
        self.assertTrue(matchObject)
        self.assertEqual(matchObject.group(1), '/boot')


    def testFailCheckTextForRemoveableDrive(self):
        blockViewer = LinuxBlockViewer()
        self.assertEquals( blockViewer.getRemoveableBlockIdText(TestLinuxBlockViewer.textNoRemoveableBlock) , [] )
        self.assertEquals( blockViewer.getRemoveableBlockIdText(TestLinuxBlockViewer.textRemoveableBlock), [ 'sdb','sdb1','sdb2'])

    def testGetFullBlockList(self):
        blockViewer = LinuxBlockViewer()
        self.assertEquals( blockViewer.getFullBlockList(TestLinuxBlockViewer.textNoRemoveableBlock) , ['sda','sda1','sda2','sda5','vagrant--vg-root','vagrant--vg-swap_1'] )
        self.assertEquals( blockViewer.getFullBlockList(TestLinuxBlockViewer.textRemoveableBlock), [ 'sda','sda1','sda2','sda5','vagrant--vg-root','vagrant--vg-swap_1','sdb','sdb1','sdb2'])
        self.assertEquals( blockViewer.getFullBlockList(TestLinuxBlockViewer.test2), [ 'sda','sda1','sda2','sda5','vagrant--vg-root','vagrant--vg-swap_1','sdb','sdb1','sdb2'])

    def testGetRemoveableDriveId(self):
        blockViewer = LinuxBlockViewer()
        self.assertEqual(blockViewer.getRemoveableDriveId(TestLinuxBlockViewer.textNoRemoveableBlock), [])
        self.assertEqual(blockViewer.getRemoveableDriveId(TestLinuxBlockViewer.textRemoveableBlock), ['sdb'])

    def testGetBlocksForDriveId(self):
        blockViewer = LinuxBlockViewer()
        self.assertEqual(blockViewer.getBlocksForDriveId(TestLinuxBlockViewer.textNoRemoveableBlock, 'sdb'), [])
        self.assertEqual(blockViewer.getBlocksForDriveId(TestLinuxBlockViewer.textRemoveableBlock, 'sdb'), ['sdb1','sdb2'])    

    def testGetMountpointForBlock(self):
        blockViewer = LinuxBlockViewer()
        self.assertEqual(blockViewer.getMountpointForBlock(TestLinuxBlockViewer.textNoRemoveableBlock, 'sda1'), ['/boot'])
        self.assertEqual(blockViewer.getMountpointForBlock(TestLinuxBlockViewer.textNoRemoveableBlock, 'sda5'), [''])


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestLinuxBlockViewer)
    unittest.TextTestRunner(verbosity=2).run(suite)