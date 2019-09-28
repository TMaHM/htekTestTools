import unittest
from data.usr_data import *


class TestMethod(unittest.TestCase):

    def test_dial(self):
        self.assertEqual(200, dut.dial(phone_2.ext))

    def test_end_call(self):
        self.assertEqual(200, dut.end_call('f4'))

    def test_set_key(self):
        self.assertTrue(True, dut.set_key(key_line=1, key_type='blf', key_value='8724', key_label='Test 1'))
        self.assertEqual(401, dut.set_key())
        self.assertEqual(404, dut.set_key(key_line=2, key_type='my test', key_mode='my test', key_value='my test'))


if __name__ == '__main__':
    unittest.main()
