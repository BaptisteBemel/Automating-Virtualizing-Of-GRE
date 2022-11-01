import netmiko

device = {}

#Try to connect to the router
try:
    #Opening of the connection
    connection = netmiko.ConnectHandler(**device)

    connection.enable()

    #The commands are being executed and the messages are printed
    connection.send_config_set(['en', 'sh ip int br'])

    #Closing of the connection
    connection.disconnect()

    print('A configuration has been pushed.')

except:
    #Unable to connect to the router
    print('The connection to the router is impossible.')
    return False