import unittest
from greca import add_route, get_config, get_network, is_in_network, validate_IP, validate_OS, validate_positive_integer, ping

class TestGreca(unittest.TestCase):

    #Test of greca.py functions

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
        self.assertTrue(validate_IP('-1.1.1.1/1'))
        self.assertTrue(validate_IP('1.1.1.1/33'))
        self.assertTrue(validate_IP('1.1.1.1/-1'))
        self.assertTrue(validate_IP('1.256.1.1/1'))
        self.assertTrue(validate_IP('0.1.1.1/1'))
        self.assertTrue(validate_IP('1.1.1.01/1'))
        self.assertTrue(validate_IP('1.1.1.4/30'))
        self.assertTrue(validate_IP('10.4.5.6/24/24'))
        self.assertTrue(validate_IP('3.4.5.6/24', True))
        self.assertFalse(validate_IP('10.4.5.6/24', True))

    def test_add_route(self):
        self.assertEqual(add_route('192.168.3.5/24', '1', '192.168.4.1', '5'), 'ip route 192.168.3.0 255.255.255.0 192.168.4.1 5')
        #afaire

    #This test needs a reachable IP address. In this example; 192.168.0.30/24
    def test_ping(self):
        self.assertFalse(ping('192.168.0.3/24'))
        self.assertTrue(ping('192.168.0.3/24'))
        self.assertTrue(ping('123.45.67.89/24'))
        
    #debug a config & copypaste on routers[] here
    def test_get_config(self):
        pass

    def test_is_in_network(self):
        self.assertFalse(is_in_network('192.168.1.1/24', '192.168.1.254/24'))
        self.assertTrue(is_in_network('192.168.1.1/25', '192.168.1.254/25'))
        self.assertTrue(is_in_network('192.168.1.1/24', '192.168.0.254/24'))
        self.assertTrue(is_in_network('192.167.1.1/24', '192.168.1.254/24'))
        self.assertTrue(is_in_network('192.168.1.1/23', '192.168.1.254/24'))

    def test_get_network(self):
        self.assertEqual(get_network('192.168.1.3/24'), '192.168.1.0')
        self.assertEqual(get_network('192.168.1.10/30'), '192.168.1.8')
        self.assertEqual(get_network('192.168.1.8/30'), '192.168.1.8')

    def test_push_config(self):
        pass

    #Test of router.py methods

    def test_get_insidePublicIP(self):
        pass

    def test_get_OS(self):
        pass

    def test_get_outsidePublicIP(self):
        pass

    def test_get_nextHop(self):
        pass

    def test_get_username(self):
        pass

    def test_get_password(self):
        pass

    def test_get_enable(self):
        pass

    def test_print(self):
        pass


    #Test of tunnel.py methods

    def test_get_name(self):
        pass

    def test_get_mtu(self):
        pass

    def test_get_keepAliveTimeOut(self):
        pass

    def test_get_keepAliveRetries(self):
        pass

    def test_get_privateIP(self):
        pass


if __name__ == '__main__':
    unittest.main()

"""
    'This IP has already been entered.'
    'Space are not allowed in the tunnel name.'
    'This tunnel name has already been entered.'
    'Maximum value is too high. It cannot exceed 10194.'
    "The subnet mask for a tunnel has to be /30."
"""