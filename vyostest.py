from netmiko import ConnectHandler

commands = ["configure", "set protocols static route 6.0.0.0/24 next-hop 3.3.3.1"]
nocommands = ["configure", "delete protocols static route 6.0.0.0/24 "]

try:
    #Opening of the connection
    connection = ConnectHandler('192.168.51.41', device_type="vyos", username="vyos", password="vyos")

    connection.enable()

    connection.send_config_set(["configure"])

    output = connection.send_command("show protocols")
    print(output)

    #The commands are being executed and the messages are printed
    connection.send_config_set(commands)

    output = connection.send_command("show protocols")
    print(output)

    connection.send_config_set(nocommands)

    output = connection.send_command("show protocols")
    print(output)

    #Closing of the connection
    connection.disconnect()
except:
    #Unable to connect to the router
    print('The connection to the router is impossible.')
