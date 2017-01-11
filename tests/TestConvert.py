import unittest
import convert


class TestCovert(unittest.TestCase):
    def test_line(self):
        input = {
            "metric": "tsd.connectionmgr.exceptions",
            "timestamp": 1484051997,
            "value": "0",
            "tags": {
                "host": "xxx",
                "type": "timeout"
            }
        }

        output = "tsd.connectionmgr.exceptions,host=xxx,type=timeout value=0 1484051997000000000"

        self.assertEqual(output, convert.line(input))

    def test_querify(self):
        self.assertEqual('', convert.querify({}))
        self.assertEqual(',a=1', convert.querify({"a": "1"}))
        self.assertEqual(',a=1,b=2', convert.querify({"a": "1", "b": "2"}))
        self.assertEqual(',a=1,b=2', convert.querify({"b": "2", "a": "1"}))
