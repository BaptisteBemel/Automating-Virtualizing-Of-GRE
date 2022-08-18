import unittest

from greca import add_route, get_config, is_in_network, validate_IP, validate_OS, validate_positive_integer

class TestGreca(unittest.TestCase):

    def test_validate_OS(self):
        self.assertFalse(validate_OS('1'))
        self.assertTrue(validate_OS('0'))
        self.assertTrue(validate_OS('4'))
        self.assertTrue(validate_OS('-2'))
        self.assertTrue(validate_OS('2.0'))
        self.assertTrue(validate_OS('a'))
        self.assertTrue(validate_OS(''))

    def test_validate_positive_integer(self):
        self.assertFalse(validate_positive_integer('1'))
        self.assertFalse(validate_positive_integer('9999'))
        self.assertTrue(validate_positive_integer('0'))
        self.assertTrue(validate_positive_integer('2.5'))
        self.assertTrue(validate_positive_integer('a'))
        self.assertTrue(validate_positive_integer(''))
        self.assertTrue(validate_positive_integer('-5'))

    def test_validate_IP(self):
        self.assertFalse(validate_IP('1.1.1.1/1'))
        self.assertTrue(validate_IP('a'))
        self.assertTrue(validate_IP('1.1.1.1/1.'))
        self.assertTrue(validate_IP('1.1.1.1/'))
        self.assertTrue(validate_IP('1.1.1.01/1/1'))
        self.assertTrue(validate_IP('1.1.1.1'))
        self.assertTrue(validate_IP('1.1.1/1'))
        self.assertTrue(validate_IP('1.1.1.1.1/1'))
        self.assertTrue(validate_IP('1.1.1.1/0'))
        self.assertTrue(validate_IP('1.1.1.1/31'))
        self.assertTrue(validate_IP('1.1.1.1/0'))
        self.assertTrue(validate_IP('1.256.1.1/1'))
        self.assertTrue(validate_IP('0.1.1.1/1'))
        self.assertTrue(validate_IP('1.1.1.01/1'))
        self.assertTrue(validate_IP('1.1.1.0/1'))

    def test_add_route(self):
        self.assertEqual(add_route('192.168.3.'), '')
        self.assertEqual(add_route(), '')
        self.assertEqual(add_route(), '')


if __name__ == '__main__':
    unittest.main()

"""
validate_IP
    validate_OS
    validate_positive_integer
    add_route
    get_config
    is_in_network
    'This IP has already been entered.'
    'Space are not allowed in the tunnel name.'
    'This tunnel name has already been entered.'
    'Maximum value is too high. It cannot exceed 10194.'
    "The subnet mask for a tunnel has to be /30."
"""