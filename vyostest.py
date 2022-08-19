from netmiko import ConnectHandler

commands = []
nocommands = []

try:
    #Opening of the connection
    connection = ConnectHandler('192.168.51.37', device_type="vyos", username="baptiste", password="GRE-Test", secret="GRE-CONFIGS")

    connection.enable()

    #The commands are being executed and the messages are printed
    connection.send_config_set(commands)

    output = connection.send_command("")
    print(output)

    connection.send_config_set(nocommands)

    output = connection.send_command("")
    print(output)

    #Closing of the connection
    connection.disconnect()
except:
    #Unable to connect to the router
    print('The connection to the router is impossible.')
