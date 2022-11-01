import unittest
from greca import add_route, get_config, get_network, is_in_network, validate_IP, validate_OS, validate_positive_integer, ping
from router import Router
from tunnel import Tunnel

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
        self.assertEqual(add_route('192.168.3.5/24', '2', '192.168.4.1', '5'), 'set protocols static route 192.168.3.0/24 next-hop 192.168.4.1 distance \'5\'')
        self.assertEqual(add_route('192.168.3.5/24', '3', '192.168.4.1', '5'), 'ip route add dst-address=192.168.3.0/24 gateway=192.168.4.1 distance=5')
        self.assertEqual(add_route('192.168.3.5/24', '1', '192.168.4.1'), 'ip route 192.168.3.0 255.255.255.0 192.168.4.1 0')
        self.assertEqual(add_route('192.168.3.5/24', '2', '192.168.4.1'), 'set protocols static route 192.168.3.0/24 next-hop 192.168.4.1 distance \'0\'')
        self.assertEqual(add_route('192.168.3.5/24', '3', '192.168.4.1'), 'ip route add dst-address=192.168.3.0/24 gateway=192.168.4.1 distance=0')

    #This test needs a reachable IP address and ping -c should be possible. In this example, the ping-able IP is: 192.168.0.3/24
    def test_ping(self):
        #self.assertFalse(ping('192.168.0.3/24'))
        self.assertTrue(ping('192.168.0.3/24'))
        self.assertTrue(ping('123.45.67.89/24'))
        
    #debug a config & copypaste on routers[] here
    def test_get_config(self):

        # Dummy variables to perform the tests

        router1 = Router('main left')
        router1.insidePublicIP = "1.1.1.2/24"
        router1.outsidePublicIP = "5.5.5.1/24"
        router1.operatingSystem = "1"
        router1.nextHop = "1.1.1.1/24"
        router1.mainRoute = "ip route 2.2.2.0 255.255.255.0 1.1.1.1 0"
        router1.backupRoute = "ip route 4.4.4.0 255.255.255.0 1.1.1.1 5"
        router1.mainGRERoute = "ip route 6.6.6.0 255.255.255.0 192.168.1.2 0"
        router1.backupGRERoute = "ip route 8.8.8.0 255.255.255.0 192.168.2.2 5"
        router1.mainTunnel = ""
        router1.backupTunnel = ""
        router1.username = "ciscoUsername"
        router1.password = "ciscoPassword"
        router1.enable = "ciscoEnable"
        router1.config = ""


        router2 = Router('main right')
        router2.insidePublicIP = "2.2.2.2/24"
        router2.outsidePublicIP = "6.6.6.1/24"
        router2.operatingSystem = "2"
        router2.nextHop = "2.2.2.1/24"
        router2.mainRoute = "set protocols static route 1.1.1.0/24 next-hop 2.2.2.1 distance \'0\'"
        router2.backupRoute = "set protocols static route 3.3.3.0/24 next-hop 2.2.2.1 distance \'5\'"
        router2.mainGRERoute = "set protocols static route 5.5.5.0/24 next-hop 192.168.1.1 distance \'0\'"
        router2.backupGRERoute = "set protocols static route 7.7.7.0/24 next-hop 192.168.3.1 distance \'5\'"
        router2.mainTunnel = ""
        router2.backupTunnel = ""
        router2.username = "vyosUsername"
        router2.password = "vyosPassword"
        router2.enable = ""
        router2.config = ""

        router3 = Router('back-up left')
        router3.insidePublicIP = "3.3.3.2/24"
        router3.outsidePublicIP = "7.7.7.1/24"
        router3.operatingSystem = "3"
        router3.nextHop = "3.3.3.1/24"
        router3.mainRoute = "ip route add dst-address=2.2.2.0/24 gateway=3.3.3.1 distance=0"
        router3.backupRoute = "ip route add dst-address=4.4.4.0/24 gateway=3.3.3.1 distance=5"
        router3.mainGRERoute = "ip route add dst-address=6.6.6.0/24 gateway=192.168.3.2 distance=0"
        router3.backupGRERoute = "ip route add dst-address=8.8.8.0/24 gateway=192.168.4.2 distance=5"
        router3.mainTunnel = ""
        router3.backupTunnel = ""
        router3.username = "mikroUsername"
        router3.password = "mikroPassword"
        router3.enable = ""
        router3.config = ""

        router4 = Router('back-up right')
        router4.insidePublicIP = "4.4.4.2/24"
        router4.outsidePublicIP = "8.8.8.1/24"
        router4.operatingSystem = "1"
        router4.nextHop = "4.4.4.1/24"
        router4.mainRoute = "ip route 1.1.1.0 255.255.255.0 4.4.4.1 0"
        router4.backupRoute = "ip route 3.3.3.0 255.255.255.0 4.4.4.1 5"
        router4.mainGRERoute = "ip route 5.5.5.0 255.255.255.0 192.168.2.1 0"
        router4.backupGRERoute = "ip route 7.7.7.0 255.255.255.0 192.168.4.1 5"
        router4.mainTunnel = ""
        router4.backupTunnel = ""
        router4.username = "cisco2Username"
        router4.password = "cisco2Password"
        router4.enable = "cisco2Enable"
        router4.config = ""

        routers = [router1, router2, router3, router4]

        tunnel1 = Tunnel('main', router1, 'main', router2, "1")
        tunnel1.name = "tun1"
        tunnel1.mtu = "1476"
        tunnel1.mss = "1436"
        tunnel1.leftPrivateIP = "192.168.1.1"
        tunnel1.rightPrivateIP = "192.168.1.2"
        tunnel1.keepAlive = "5 4"
        tunnel1.keepAliveTimeOut = "5"
        tunnel1.keepAliveRetries = "4"

        tunnel2 = Tunnel('backup', router1, 'main', router4, "2")
        tunnel2.name = "tun2"
        tunnel2.mtu = "1476"
        tunnel2.mss = "1436"
        tunnel2.leftPrivateIP = "192.168.2.1"
        tunnel2.rightPrivateIP = "192.168.2.2"
        tunnel2.keepAlive = "5 4"
        tunnel2.keepAliveTimeOut = "5"
        tunnel2.keepAliveRetries = "4"

        tunnel3 = Tunnel('main', router3, 'backup', router2, "3")
        tunnel3.name = "tun3"
        tunnel3.mtu = "1476"
        tunnel3.mss = "1436"
        tunnel3.leftPrivateIP = "192.168.3.1"
        tunnel3.rightPrivateIP = "192.168.3.2"
        tunnel3.keepAlive = "5 4"
        tunnel3.keepAliveTimeOut = "5"
        tunnel3.keepAliveRetries = "4"

        tunnel4 = Tunnel('backup', router3, 'backup', router4, "4")
        tunnel4.name = "tun4"
        tunnel4.mtu = "1476"
        tunnel4.mss = "1436"
        tunnel4.leftPrivateIP = "192.168.4.1"
        tunnel4.rightPrivateIP = "192.168.4.2"
        tunnel4.keepAlive = "5 4"
        tunnel4.keepAliveTimeOut = "5"
        tunnel4.keepAliveRetries = "4"


        allTunnels = [tunnel1, tunnel2, tunnel3, tunnel4]

        router1.mainTunnel = tunnel1
        router1.backupTunnel = tunnel2
        router2.mainTunnel = tunnel1
        router2.backupTunnel = tunnel3
        router3.mainTunnel = tunnel3
        router3.backupTunnel = tunnel4
        router4.mainTunnel = tunnel2
        router4.backupTunnel = tunnel4

        routers = routers

        """self.assertEqual(get_config(routers, 1, False), [
            'configure terminal', "ip route 2.2.2.0 255.255.255.0 1.1.1.1 0", 
            "ip route 4.4.4.0 255.255.255.0 1.1.1.1 5", "ip route 6.6.6.0 255.255.255.0 192.168.1.2 0",
            "ip route 8.8.8.0 255.255.255.0 192.168.2.2 5",
            'interface tunnel tun1', 
            'ip mtu 1476', 
            'ip tcp adjust-mss 1436',
            'ip address 192.168.1.1 255.255.255.252',
            'tunnel source 1.1.1.2', 
            'tunnel destination 2.2.2.2',
            'keepalive 5 4', 
            'interface tunnel tun2',
            'ip mtu 1476', 
            'ip tcp adjust-mss 1436',
            'ip address 192.168.2.1 255.255.255.252',
            'tunnel source 1.1.1.2', 
            'tunnel destination 4.4.4.2',
            'keepalive 5 4',
            'wr'
            ])"""

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

    #Informations about the routers shall be correct
    def test_push_config(self):
        pass


if __name__ == '__main__':
    unittest.main()