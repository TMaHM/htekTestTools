import unittest
from data.usr_data import *


class TestMethod(unittest.TestCase):

    def test_dial(self):
        self.assertEqual(200, dut.dial(phone_2.ext))

    def test_end_call(self):
        self.assertEqual(200, dut.end_call('f4'))


if __name__ == '__main__':
    unittest.main()
