from netmiko import ConnectHandler

commands = ["ip route add dst-address=6.0.0.0/24 gateway= "]
nocommands = ["ip route remove [find dst-address=6.0.0.0/24]"]

mikro = {
    'ip': '192.168.51.45',
    'device_type': "mikrotik_routeros",
    'username': "admin",
    'password': "GRE-Test",
}

#try:
#Opening of the connection
connection = ConnectHandler(**mikro)

connection.enable()

output = connection.send_command("/ip route print")
print(output)

#The commands are being executed and the messages are printed
connection.send_config_set(commands)

output = connection.send_command("/ip route print")
print(output)

connection.send_config_set(nocommands)

output = connection.send_command("ip route print")
print(output)

#Closing of the connection
connection.disconnect()
#except:
    #Unable to connect to the router
 #   print('The connection to the router is impossible.')
