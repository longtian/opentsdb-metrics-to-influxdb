import unittest
import convert


class TestCovert(unittest.TestCase):
    def test_convert(self):
        input = {
            "metric": "tsd.connectionmgr.exceptions",
            "timestamp": 1484051997,
            "value": "0",
            "tags": {
                "host": "xxx",
                "type": "timeout"
            }
        }

        output = "tsd.connectionmgr.exceptions,type=timeout,host=xxx value=0 1484051997000000000"

        self.assertEqual(output, convert.convert(input))
