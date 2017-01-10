import unittest
import convert


class TestCovert(unittest.TestCase):
    def test_convert(self):
        input = "tsd.connectionmgr.connections 1484040264 32942 type=open host=xxx"
        output = "tsd.connectionmgr.connections,type=open,host=xxx value=32942 1484040264000000000"

        self.assertEqual(output, convert.convert(input))
