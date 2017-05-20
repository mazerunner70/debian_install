import unittest
from FormatSd import FormatSdCard

class FormatSdTest(unittest.TestCase):

    textLine = '432013312 bytes (432 MB, 412 MiB) copied, 62.5562 s, 6.9 MB/s\n'
    

    def testCalculateProgress(self):
        formatSd = FormatSdCard()
        imageSize = 1000*1000*1000
        self.assertEqual(formatSd.calculateProgress(FormatSdTest.textLine, imageSize), 43)




if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(FormatSdTest)
    unittest.TextTestRunner(verbosity=2).run(suite)