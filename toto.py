import netmiko

device = {'ip': '192.168.51.38', 'device_type': 'cisco_ios',
          'username': 'baptiste', 'password': 'GRE-Test', 'secret': ''}
config = ['configure terminal', 'ip route 2.2.2.0 255.255.255.0 1.1.1.1 0', 'ip route 3.3.3.0 255.255.255.0 1.1.1.1 5', 'ip route 7.7.7.0 255.255.255.0 192.168.102.1 0', 'ip route 8.8.8.0 255.255.255.0 192.168.104.1 5', 'interface tunnel 2', 'ip mtu 1476', 'ip tcp adjust-mss 1436', 'ip address 192.168.102.2 255.255.255.252', 'tunnel source 1.1.1.2', 'tunnel destination 2.2.2.2', 'keepalive 5 4', 'interface tunnel 4',
          'ip mtu 1476', 'ip tcp adjust-mss 1436', 'ip address 192.168.104.2 255.255.255.252', 'tunnel source 1.1.1.2', 'tunnel destination 3.3.3.2', 'keepalive 5 4', 'interface out int', 'ip nat inside', 'exit', 'interface int int', 'ip nat outside', 'exit', 'access-list 1 permit 15.15.15.0 0.0.0.255', 'ip nat pool poolName 15.15.15.15 15.15.15.30', 'ip nat inside source list 1 pool poolName', 'end', 'wr']

# Try to connect to the router
try:
    # Opening of the connection
    connection = netmiko.ConnectHandler(**device)
    print('1')

    connection.enable()
    print('2')

    # The commands are being executed and the messages are printed
    connection.send_config_set(config)
    print('3')

    # Closing of the connection
    connection.disconnect()

    print('A configuration has been pushed.')

except:
    # Unable to connect to the router
    print('The connection to the router is impossible.')
