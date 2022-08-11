# Baptiste Bemelmans - GRECA: Generic Routing Encapsulation Configuration Assistant - For SatADSL - made in August 2022
from msilib.schema import Error
from re import A, S
from select import select
from urllib import response
import netmiko
import subprocess


def main():
    
    for turn in range(4):
        #Public IP of the routers
        if turn == 0:
            print('Informations about the main local router')
        elif turn == 1:
            print('Informations about the main remote router')
        elif turn == 2:
            print('Informations about the back-up local router')
        elif turn == 3:
            print('Informations about the back-up remote router')

        while True:
            again = False

            publicIPMask = input("Enter the public IP/mask of the router: ")

            #Validate the format of the public IP
            again = validate_IP(publicIPMask)

            """
            #Ping the first router
            if not again:
                again = ping(publicIP)"""


            if not again:
                break


        #OS of the routers
        while True:
            again = False
                    
            OS = input("Enter the OS of the router ('1': CSR, '2': VyOS, '3': Mikrotik): ")

            #Validate the format of the public IP
            again = validate_OS(OS)


            if not again:
                break

        if turn == 0:
            mainLocalPublicIPMask = publicIPMask
            mainLocalOS = OS

        elif turn == 1:
            mainRemotePublicIPMask = publicIPMask
            mainRemoteOS = OS

        elif turn == 2:
            backupLocalPublicIPMask = publicIPMask
            backupLocalOS = OS

        elif turn == 3:
            backupRemotePublicIPMask = publicIPMask
            backupRemoteOS = OS

    

    #Adding routes
    for turn in range(8):

        if turn == 0:
            routerSelector = "local main"
            nextHopSelector = "Main next-hop"
        elif turn == 1:
            routerSelector = "local main"
            nextHopSelector = "Back-up next-hop"
        elif turn == 2:
            routerSelector = "remote main"
            nextHopSelector = "Main next-hop"
        elif turn == 3:
            routerSelector = "remote main"
            nextHopSelector = "Back-up" 
        elif turn == 4:
            routerSelector = "local back-up"
            nextHopSelector = "Main route"
        elif turn == 1:
            routerSelector = "local back-up"
            nextHopSelector = "Back-up route"
        elif turn == 2:
            routerSelector = "remote back-up"
            nextHopSelector = "Main route"
        elif turn == 3:
            routerSelector = "remote back-up"
            nextHopSelector = "Back-up route" 


        while True:
            again = False
                
            nextHop = input(nextHopSelector + " gateway of the " + routerSelector + " router : ")

            again = validate_IP(nextHop)

            if not again:
                break
        
        
        if not again and routerSelector == "1st" and gatewaySelector == "Main":
            firstMainRoute = add_route(mainRemotePublicIPMask, firstOS, nextHop)
        
        elif not again and routerSelector == "1st" and gatewaySelector == "Back-up":
            firstBackupRoute = add_route(mainRemotePublicIPMask, firstOS, nextHop, '5')

        elif not again and routerSelector == "2nd" and gatewaySelector == "Main":
            secondMainRoute = add_route(mainLocalPublicIPMask, secondOS, nextHop)

        elif not again and routerSelector == "2nd" and gatewaySelector == "Back-up":
            secondBackupRoute = add_route(mainLocalPublicIPMask, secondOS, nextHop, '5')


    #Tunnels
    for turn in range(4):

        if turn == 0:
            routerSelector = "1st"
            tunnelSelector = "main"
        elif turn == 1:
            tunnelSelector = "back-up"
        elif turn == 2:
            routerSelector = "2nd"
            tunnelSelector = "main"
        elif turn == 3:
            tunnelSelector = "back-up" 

        if turn == 0 or turn == 2:
            #Name of the GRE tunnel
            tunnel = input("Enter the name of the " + tunnelSelector + " tunnel (default name: [insert generated tunnel name]): ")

            while True:
                keepAliveTimeOut = input("Enter the number of seconds for the keep-alive for the " + tunnelSelector + " tunnel (default time: 5(seconds)): ")
                again = validate_positive_integer(keepAliveRetries)
                if not again:
                    break

            while True: 
                keepAliveRetries = input("Enter the number of retries for the " + tunnelSelector + " tunnel (default number: 4): ")
                again = validate_positive_integer(keepAliveRetries)
                if not again:
                    break


        #Private IPs
        while True:
            again = False

            privateIPMask = input("Enter the private IP/mask of the " + routerSelector + " router for the " + tunnelSelector + " tunnel: ")

            #Validate the format of the private
            again = validate_IP(privateIPMask)

            if not again:
                if privateIPMask.split('/')[1] == "30":
                    break
                else:
                    print("The subnet mask for a tunnel has to be /30.")


        if turn == 0:
            tunnel1 = tunnel
            keepAliveTimeOut1 = keepAliveTimeOut
            keepAliveRetries1 = keepAliveRetries
            firstMainIPMask = privateIPMask

        elif turn == 1:
            secondMainIPMask = privateIPMask
        
        elif turn == 2:
            tunnel2 = tunnel
            keepAliveTimeOut2 = keepAliveTimeOut
            keepAliveRetries2 = keepAliveRetries
            firstBackupIPMask = privateIPMask
        
        elif turn == 3:
            secondBackupIPMask = privateIPMask

    values = {
        "mainLocalPublicIPMask": mainLocalPublicIPMask,
        "firstMainPrivateIPMask": firstMainIPMask,
        "firstBackupPrivateIPMask": firstBackupIPMask,
        "firstOS": firstOS,
        "firstMainRoute": firstMainRoute,
        "firstBackupRoute": firstBackupRoute,
        "mainRemotePublicIPMask": mainRemotePublicIPMask,
        "secondMainPrivateIPMask": secondMainIPMask,
        "secondBackupPrivateIPMask": secondBackupIPMask,
        "secondOS": secondOS,
        "secondMainRoute": secondMainRoute,
        "secondBackupRoute": secondBackupRoute,
        "mainTunnel": tunnel1,
        "backupTunnel": tunnel2,
        "keepAlive": keepAliveTimeOut1 + ' ' + keepAliveRetries1,
        "keepAlive2": keepAliveTimeOut2 + ' ' + keepAliveRetries2
    }

    config_router1 = get_config(values, 1)
    config_router2 = get_config(values, 2)





#documentation
def validate_IP(ipMask):

    #The first input contains both the customer IP and the subnet mask. This input has to be divided based on the slash.
    inputTest = ipMask.split('/')

    #The first input cannot take more than a slash
    if len(inputTest) != 2:
        print('The input was written incorrectly. The subnet mask has to be written with a slash. Ex: 197.164.73.5/24')
        return True

    #Test the IP and the mask
    ipTest = inputTest[0]
    maskTest = inputTest[1]
    ipTestClasses = ipTest.split('.')
    customer_network_address = ''
    
    #The IP's are divided into classes. There must be four classes per IP
    if len(ipTestClasses) != 4:
        print('The IP has been written incorrectly. Ex: 197.164.73.5/24')
        return True

    #There must be only one part to the mask
    try:
        if len(maskTest) == 0 or not (int(maskTest) >= 1 and int(maskTest) <= 32):
            print('The mask has been written incorrectly. Ex: 197.164.73.5/24')
            return True
    except ValueError:
        print('The mask has been written incorrectly. Ex: 197.164.73.5/24')
        return True

    for ipClass in range(len(ipTestClasses)):
        try:
            #The classes must be numbers between 0 and 255
            if not (int(ipTestClasses[ipClass]) >= 0 and int(ipTestClasses[ipClass]) <= 255):
                print('The IP has been written incorrectly. Ex: 197.164.73.5/24')
                return True
            #Forbids useless "0"
            elif len(ipTestClasses[ipClass]) > 1 and ipTestClasses[ipClass][0] == '0':
                print('The IP has been written incorrectly. Ex: 197.164.73.5/24 Useless "0" must be removed.')
                return True                   
            #The IP cannot finish by 0
            elif ipClass == 3 and int(ipTestClasses[ipClass]) == 0:
                print('The IP cannot finish by 0')
                return True
        except:
            print('The IP has been written incorrectly. Ex: 197.164.73.5/24')
            return True


#documentation
def ping(host):
    print('Pinging...')
    try:
        output = subprocess.check_output("ping " + host, shell=True)
        output = output.decode('windows-1252')
        
        #Only works in french and english - If the system is in another language, it might not detect "Destination Host Unreachable" - The d is not written because it's a capital in english a small in french.
        if "estination" in output:
            print('The router cannot be ping. Destination Host Unreachable')
            return True
        
        #Correct - Ping is working
        return False


    except subprocess.CalledProcessError:
        print('The router cannot be ping. Request Timed Out')
        return True
    

#documentation
def validate_OS(osInput):
    try:
        if not (int(osInput) >= 1 and int(osInput) <= 3):
            print('The OS number has been written incorrectly. Please type 1 (CSR), 2 (VyOS) or 3 (Mikrotik)')
            return True
        
        return False
    except ValueError:
        print('The OS number has been written incorrectly. Please type 1 (CSR), 2 (VyOS) or 3 (Mikrotik)')
        return True

#add documentation
def add_route(targetIPMask, firstOS, nextHop, distance='1'):

    #Translation from /subnet_mask to a classic subnet mask
    traduction_subnet_mask = {
        '1': '128.0.0.0',
        '2': '192.0.0.0',
        '3': '224.0.0.0',
        '4': '224.0.0.0',
        '5': '248.0.0.0',
        '6': '252.0.0.0',
        '7': '254.0.0.0',
        '8': '255.0.0.0',
        '9': '255.128.0.0',
        '10': '255.192.0.0',
        '11': '255.224.0.0',
        '12': '255.240.0.0',
        '13': '255.248.0.0',
        '14': '255.252.0.0',
        '15': '255.254.0.0',
        '16': '255.255.0.0',
        '17': '255.255.128.0',
        '18': '255.255.192.0',
        '19': '255.255.224.0',
        '20': '255.255.240.0',
        '21': '255.255.248.0',
        '22': '255.255.252.0',
        '23': '255.255.254.0',
        '24': '255.255.255.0',
        '25': '255.255.255.128',
        '26': '255.255.255.192',
        '27': '255.255.255.224',
        '28': '255.255.255.240',
        '29': '255.255.255.248',
        '30': '255.255.255.252',
        '31': '255.255.255.254',
        '32': '255.255.255.255',
    }

    #Get the network address of the customer
    targetIPSplit = targetIPMask.split('/')[0].split('.')
    targetMask = traduction_subnet_mask[targetIPMask.split('/')[1]]
    targetNetwork = targetIPSplit[0:3]
    targetNetwork.append('0')
    juncture = '.'
    targetNetwork = juncture.join(targetNetwork)
    listNetworkMask = [targetNetwork, targetIPMask.split('/')[1]]
    juncture = '/'
    targetNetworkMask = juncture.join(listNetworkMask)

    #CSR
    if firstOS == '1':
        new_route = 'ip route ' + targetNetwork + ' ' + targetMask + ' ' + nextHop + ' ' + distance

    #VyOS
    elif firstOS == '2':
        new_route = 'set protocols static route ' + targetNetworkMask + ' next-hop ' + nextHop + ' distance \'' + distance + '\''

    #Mikrotik
    elif firstOS == '3':
        new_route = 'ip route add dst-address=' + targetNetworkMask + ' gateway=' + nextHop + ' distance=' + distance
    
    return new_route


def validate_positive_integer(stringNumber):
    try:
        if not int(stringNumber) >= 0:
                print('The input has to be a positive integer')
                return True

    except ValueError:
        print("The input is not an integer. Try again.")
        return True
    


def get_config(values, router):
    if router == 1:
        selector = "first"
        otherRouter = "second"
    elif router == 2:
        selector = "second"
        otherRouter = "first"

    #CSR
    if values[selector + "OS"] == '1':
        config = [
            'enable', 'configure terminal', values[selector + "MainRoute"], 
            values[selector + "BackupRoute"], 'interface tunnel ' + values["mainTunnel"], 
            'ip address ' + values[selector + "MainPrivateIPMask"].split('/')[0] + ' 255.255.255.252',
            'tunnel source ' + values[selector + "PublicIPMask"], 
            'tunnel destination ' + values[otherRouter + "PublicIPMask"],
            'keepalive ' + values["keepAlive"], 'interface tunnel ' + values["backupTunnel"], 
            'ip address ' + values[selector + "BackupPrivateIPMask"].split('/')[0] + ' 255.255.255.252',
            'tunnel source ' + values[selector + "PublicIPMask"], 
            'tunnel destination ' + values[otherRouter + "PublicIPMask"],
            'keepalive ' + values["keepAlive"],

            ]

    #VyOS
    elif values[selector + "OS"] == '2':
        pass        

    #Mikrotik
    elif values[selector + "OS"] == '3':
        pass


"""
#List of commands to run on the routeur
commands = ['enable', 'configure terminal', new_route]

#Try to connect to the router
try:
    #Opening of the connection
    connection = netmiko.ConnectHandler(ip=customer_default_gateway_ip_address, device_type="cisco_ios", username="", password="")

    #The commands are being executed and the messages are printed
    print(connection.send_config_set(commands))

    #Closing of the connection
    connection.disconnect()
except:
    #Unable to connect to the router
    print('The connection to the router is impossible.')
    return False
    """


if __name__ == '__main__':
    main()
