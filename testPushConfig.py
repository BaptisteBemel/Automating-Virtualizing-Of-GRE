import netmiko

configs = [['enable', 'configure terminal', 'ip route 2.2.2.0 255.255.255.0 1.1.1.1/24 1', 'ip route 4.4.4.0 255.255.255.0 1.1.1.1/24 5', 'ip route 6.6.6.0 255.255.255.0 192.168.1.2/30 1', 'ip route 8.8.8.0 255.255.255.0 192.168.2.2/30 5', 'interface tunnel tun1', 'ip mtu 1476', 'ip tcp adjust-mss 1436', 'ip address 192.168.1.1 255.255.255.252', 'tunnel source 1.1.1.2', 'tunnel destination 2.2.2.2', 'keepalive 5 4', 'interface tunnel tun2', 'ip mtu 1476', 'ip tcp adjust-mss 1436', 'ip address 192.168.2.1 255.255.255.252', 'tunnel source 1.1.1.2', 'tunnel destination 4.4.4.2', 'keepalive 5 4', 'wr'], ['configure', "set protocols static route 1.1.1.0/24 next-hop 2.2.2.1/24 distance '1'", "set protocols static route 3.3.3.0/24 next-hop 2.2.2.1/24 distance '5'", "set protocols static route 5.5.5.0/24 next-hop 192.168.1.1/30 distance '1'", "set protocols static route 7.7.7.0/24 next-hop 192.168.3.1/30 distance '5'", 'set interfaces tunnel tun1 address 192.168.1.2/30', 'set interfaces tunnel tun1 encapsulation gre', 'set interfaces tunnel tun1 mtu 1476', 'set firewall options tun1 adjust-mss 1436', 'set interfaces tunnel tun1 local-ip 2.2.2.2', 'set interfaces tunnel tun1 remote-ip 1.1.1.2', 'set interfaces tunnel tun3 address 192.168.3.2/30', 'set interfaces tunnel tun3 encapsulation gre', 'set interfaces tunnel tun3 mtu 1476', 'set firewall options tun3 adjust-mss 1436', 'set interfaces tunnel tun3 local-ip 3.3.3.2', 'set interfaces tunnel tun3 remote-ip 5 4', 'commit', 'save'], ['configure', 'ip route add dst-address=2.2.2.0/24 gateway=3.3.3.1/24 distance=1', 'ip route add dst-address=4.4.4.0/24 gateway=3.3.3.1/24 distance=5', 'ip route add dst-address=6.6.6.0/24 gateway=192.168.3.2/30 distance=1', 'ip route add dst-address=8.8.8.0/24 gateway=192.168.4.2/30 distance=5', '/interface gre add name=tun3 remote-address=2.2.2.2 local-address=3.3.3.2', '/interface gre set name=tun3 mtu=1476', '/ip firewall mangle add out-interface=tun3 protocol=tcp tcp-flags=syn action=change-mss new-mss=1436 chain=forward tcp-mss=1437-65535', '/ip address  add address=192.168.3.1/30 interface=tun3', '/interface gre add name=tun4 remote-address=4.4.4.2 local-address=3.3.3.2', '/interface gre set name=tun4 mtu=1476', '/ip firewall mangle add out-interface=tun4 protocol=tcp tcp-flags=syn action=change-mss new-mss=1436 chain=forward tcp-mss=1437-65535', '/ip address  add address=192.168.4.1/30 interface=tun4'], ['enable', 'configure terminal', 'ip route 1.1.1.0 255.255.255.0 4.4.4.1/24 1', 'ip route 3.3.3.0 255.255.255.0 4.4.4.1/24 5', 'ip route 5.5.5.0 255.255.255.0 192.168.2.1/30 1', 'ip route 7.7.7.0 255.255.255.0 192.168.4.1/30 5', 'interface tunnel tun2', 'ip mtu 1476', 'ip tcp adjust-mss 1436', 'ip address 192.168.2.2 255.255.255.252', 'tunnel source 4.4.4.2', 'tunnel destination 1.1.1.2', 'keepalive 5 4', 'interface tunnel tun4', 'ip mtu 1476', 'ip tcp adjust-mss 1436', 'ip address 192.168.4.2 255.255.255.252', 'tunnel source 4.4.4.2', 'tunnel destination 3.3.3.2', 'keepalive 5 4', 'wr']]

def push_config(configs):    
    for config in range(len(configs)):
        if config.operatingSystem == '1':
            device = {
            'ip': config.insidePublicIP,
            'device_type': "cisco_ios",
            'username': config.username,
            'password': config.password,
            'secret': config.enable
        }
        elif config.operatingSystem == '2':
            device = {
            'ip': config.insidePublicIP,
            'device_type': "vyos",
            'username':   config.username,
            'password':   config.password,
        }
        else:
            device = {
            'ip': configs.insidePublicIP,
            'device_type': "mikrotik_routeros",
            'username':   configs.username,
            'password':   configs.password,
        }


        #Try to connect to the router
        try:
            #Opening of the connection
            connection = netmiko.ConnectHandler(**device)

            connection.enable()

            #The commands are being executed and the messages are printed
            print(connection.send_config_set(config))

            #Closing of the connection
            connection.disconnect()
        except:
            #Unable to connect to the router
            print('The connection to the router is impossible.')
            return False
