from netmiko import ConnectHandler

commands = ["configure terminal", "ip route 6.0.0.0 255.255.255.0 2.2.2.1", "wr"]
nocommands = ["configure terminal", "no ip route 6.0.0.0 255.255.255.0 2.2.2.1", "wr"]

try:
    #Opening of the connection
    connection = ConnectHandler('192.168.51.37', device_type="cisco_ios", username="baptiste", password="GRE-Test", secret="GRE-CONFIGS")

    connection.enable()

    output = connection.send_command("show ip route")
    print(output)

    #The commands are being executed and the messages are printed
    connection.send_config_set(commands)

    output = connection.send_command("show ip route")
    print(output)

    connection.send_config_set(nocommands)

    output = connection.send_command("show ip route")
    print(output)

    #Closing of the connection
    connection.disconnect()
except:
    #Unable to connect to the router
    print('The connection to the router is impossible.')
