# Baptiste Bemelmans - GRECA: Generic Routing Encapsulation Configuration Assistant - For SatADSL
from posixpath import split
import re
import netmiko
import subprocess
from router import Router
from tunnel import Tunnel
import os


def main():
    allIP = []

    router1 = Router('main left')
    router2 = Router('main right')
    router3 = Router('back-up left')
    router4 = Router('back-up right')

    routers = [router1, router2, router3, router4]
    for turn in range(4):
        #Public IP of the routers
        while True:
            again = False

            publicIPMask = routers[turn].get_insidePublicIP()

            #Validate the format of the public IP
            #again = validate_IP(publicIPMask)

            if publicIPMask in allIP:
                print('This IP has already been entered.') 
                again = True

            if not again:
                pass
                #again = ping(publicIPMask)

            if not again:
                allIP.append(publicIPMask)
                break


        #OS of the routers
        while True:
            again = False
  
            OS = routers[turn].get_OS() 

            #Validate the format of the public IP
            again = validate_OS(OS)

            if not again:
                break


        #Outside IP
        while True:
            again = False
  
            outsidePublicIP = routers[turn].get_outsidePublicIP() 

            #Validate the format of the public IP
            #again = validate_IP(outsidePublicIP)

            if outsidePublicIP in allIP:
                print('This IP has already been entered.') 
                again = True

            if not again:
                break

        #Username
        while True:
            again = False
  
            username = routers[turn].get_username() 

            if not re.match("^[A-Za-z0-9_-]*$", username):
                print("This input can only contains capital and small letters, numbers, underscore and dashes.")
                again = True

            if not again:
                break

        #Password
        while True:
            again = False
  
            password = routers[turn].get_password() 

            if not re.match("^[A-Za-z0-9_-]*$", password):
                print("This input can only contains capital and small letters, numbers, underscore and dashes.")
                again = True

            if not again:
                break

        #Enable if cisco
        if OS == '1':
            while True:
                again = False
    
                enable = routers[turn].get_enable() 

                if not re.match("^[A-Za-z0-9_-]*$", enable):
                    print("This input can only contains capital and small letters, numbers, underscore and dashes.")
                    again = True

                if not again:
                    break
    

    #Adding routes
    for turn in range(4):

        while True:
            again = False
                
            nextHop = routers[turn].get_nextHop()

            #again = validate_IP(nextHop)

            if nextHop in allIP :
                print('This IP has already been entered.') 
                again = True


            if not again:
                if not is_in_network(routers[turn].insidePublicIP, nextHop):
                    break

        if turn % 2 == 0:
            routers[turn].mainRoute = add_route(routers[1].insidePublicIP, routers[turn].operatingSystem, nextHop)
            routers[turn].backupRoute = add_route(routers[3].insidePublicIP, routers[turn].operatingSystem, nextHop, '5')
        else:
            routers[turn].mainRoute = add_route(routers[0].insidePublicIP, routers[turn].operatingSystem, nextHop)
            routers[turn].backupRoute = add_route(routers[2].insidePublicIP, routers[turn].operatingSystem, nextHop, '5')


    #Tunnels, private IPs, keep-alive
    tunnel1 = Tunnel('main', router1, 'main', router2)
    tunnel2 = Tunnel('backup', router1, 'main', router4)
    tunnel3 = Tunnel('main', router3, 'backup', router2)
    tunnel4 = Tunnel('backup', router3, 'backup', router4)

    allTunnels = [tunnel1, tunnel2, tunnel3, tunnel4]

    router1.mainTunnel = tunnel1
    router1.backupTunnel = tunnel2
    router2.mainTunnel = tunnel1
    router2.backupTunnel = tunnel3
    router3.mainTunnel = tunnel3
    router3.backupTunnel = tunnel4
    router4.mainTunnel = tunnel2
    router4.backupTunnel = tunnel4
    
    
    for turn in range(4):

        while True:
            #Name of the GRE tunnel

            tunnel = allTunnels[turn].get_name()

            if not re.match("^[A-Za-z0-9_-]*$", tunnel):
                print("This input can only contains capital and small letters, numbers, underscore and dashes.")
                again = True
            
            if tunnel in allTunnels :
                print('This tunnel name has already been entered.') 
                again = True

            if not again:
                allTunnels.append(tunnel)
                break


        while True:
            mtu = allTunnels[turn].get_mtu()
            again = validate_positive_integer(mtu)

            if not again:
                if int(mtu) > 2000 or int(mtu) < 1000:
                    print('This value is not correct. It has to be between 1000 and 2000.')
                else:
                    break


        while True:
            keepAliveTimeOut = allTunnels[turn].get_keepAliveTimeOut()

            again = validate_positive_integer(keepAliveTimeOut)

            if not again:
                if int(keepAliveTimeOut) > 5:
                    print('This value is not correct. It cannot be above 5.')
                else:
                    break


        while True: 
            keepAliveRetries = allTunnels[turn].get_keepAliveRetries()

            again = validate_positive_integer(keepAliveRetries)

            if not again:
                if int(keepAliveRetries) > 5:
                    print('This value is not correct. It cannot be above 5.')
                else:
                    break

    privateIPs = []
    for turn in range(4):

        #Private IPs
        for routerTurn in range(2):
            while True:
                again = False

                if routerTurn == 0:
                    privateIPMask = allTunnels[turn].get_privateIP('left')
                else:
                    privateIPMask = allTunnels[turn].get_privateIP('right')

                #Validate the format of the private
                #again = validate_IP(privateIPMask, True)

                if privateIPMask in privateIPs or privateIPMask in allIP:
                    print('This private IP has already been entered.') 
                    again = True

                if routerTurn == 1:
                    again = is_in_network(privateIPs[len(privateIPs)-1], privateIPMask)

                if not again:
                    if privateIPMask.split('/')[1] == "30":
                        privateIPs.append(privateIPMask)
                        break
                    else:
                        print("The subnet mask for a tunnel has to be /30.") 

    for turn in range(4):

        if turn % 2 == 0:
            routers[turn].mainGRERoute = add_route(routers[1].outsidePublicIP, routers[turn].operatingSystem, routers[turn].mainTunnel.rightPrivateIP)
            routers[turn].backupGRERoute = add_route(routers[3].outsidePublicIP, routers[turn].operatingSystem, routers[turn].backupTunnel.rightPrivateIP, '5')
        else:
            routers[turn].mainGRERoute = add_route(routers[0].outsidePublicIP, routers[turn].operatingSystem, routers[turn].mainTunnel.leftPrivateIP)
            routers[turn].backupGRERoute = add_route(routers[2].outsidePublicIP, routers[turn].operatingSystem, routers[turn].backupTunnel.leftPrivateIP, '5')   


    configs = []

    for turn in range(4):
        routers[turn].config = get_config(routers, turn + 1)
        configs.append([routers[turn], routers[turn].config])  

    #The software shall be used onto linux OS. If another OS is used, change the command below to clear the terminal
    os.system("clear")  

    router1.print()
    router2.print()
    router3.print()
    router4.print()

    while True:
            again = False
  
            confirm = input("Do you confirm the configurations ? (yes/no): ")

            if confirm == "yes":
                push_config(configs)
            elif confirm == "no":
                while True:
                    sureAgain = False
                    sure = input("Are you sure you want to cancel the configuration ? (yes/no): ")

                    if sure == "yes":
                        pass
                    elif sure == "no":
                        again = True
                    else:
                        sureAgain = True

                    if not sureAgain:
                        print("Please enter 'yes' or 'no'")
                        break
            else:
                print("Please enter 'yes' or 'no'")
                again = False

            if not again:
                break



def validate_IP(ipMask, isPrivate=False):
    """This function verifies if an entered IP address has the correct format. 
    The correct format in this case being: x.x.x.x/y 

    Args:
        ipMask (string): This string has the value of an IP address and a subnet mask.

    Returns:
        boolean: If any of the rules to write an IP address with its subnet mask is not respected, the function returns True. Otherwise, it returns False.
    """

    #The argument contains both the IP address and the subnet mask. It has to be divided based on the slash in order to be tested.
    inputTest = ipMask.split('/')

    #If the arguments doesn't have a backslash or has more than one, the format is incorrect.
    if len(inputTest) != 2:
        print('The input was written incorrectly. The subnet mask has to be written with a slash. Ex: 197.164.73.5/24')
        return True

    #Test the IP and the subnet mask. The IP address is devided into classes so that each one can be tested.
    ipTest = inputTest[0]
    maskTest = inputTest[1]
    ipTestClasses = ipTest.split('.')
    
    #The IP's are divided into classes. There must be four classes per IP address.
    if len(ipTestClasses) != 4:
        print('The IP has been written incorrectly. Ex: 197.164.73.5/24')
        return True

    #There must be only one part to the mask.
    try:
        if len(maskTest) == 0 or not (int(maskTest) >= 0 and int(maskTest) <= 32):
            print('The mask has been written incorrectly. Ex: 197.164.73.5/24')
            return True
    except ValueError:
        print('The mask has been written incorrectly. Ex: 197.164.73.5/24')
        return True

    #Each class is being tested.
    for ipClass in range(len(ipTestClasses)):
        try:
            #The classes must be numbers between 0 and 255.
            if not (int(ipTestClasses[ipClass]) >= 0 and int(ipTestClasses[ipClass]) <= 255):
                print('The IP has been written incorrectly. Ex: 197.164.73.5/24')
                return True
            #Forbids useless "0" at the beginning of a class.
            elif len(ipTestClasses[ipClass]) > 1 and ipTestClasses[ipClass][0] == '0':
                print('The IP has been written incorrectly. Ex: 197.164.73.5/24 Useless "0" must be removed.')
                return True               
            elif ipTest == get_network(ipMask):
                print('The IP address cannot be the network address.')
                return True
            elif (ipClass == 0 and ipTestClasses[ipClass] == '0') or (ipClass == 0 and int(ipTestClasses[ipClass])  > 223):
                print("The first class cannot be 0 or above 223.")
                return True
        except:
            print('The IP has been written incorrectly. Ex: 197.164.73.5/24')
            return True

    if not (get_network(ipTest + '/8') == '10.0.0.0' or get_network(ipTest + '/12') == '172.16.0.0' or get_network(ipTest + '/16') == '192.168.0.0' or get_network(ipTest + '/4') == '224.0.0.0') and isPrivate:
        print('The private IP is not within a correct private IP\'s range')
        return True
    elif not isPrivate and (get_network(ipTest + '/8') == '10.0.0.0' or get_network(ipTest + '/12') == '172.16.0.0' or get_network(ipTest + '/16') == '192.168.0.0' or get_network(ipTest + '/4') == '224.0.0.0'):
        print('The public IP cannot be in the private IP\'s range')
        return True


def ping(host):
    """This function uses the subprocess library to executes a ping command with the user's machine.

    Args:
        host (string): This string has the value of the inside IP address and the subnet mask of a router.

    Returns:
        boolean: If the ping fails, it returns True. If it passes, it returns False.
    """
    print('Pinging...')
    try:
        #It performs 3 ping request to the target "host" device.
        output = subprocess.check_output("ping -c 3 " + host.split('/')[0], shell=True)
        #subprocess.check_output() returns a binary that has to be decoded. windows-1252 accepts characters from more languages than utf-8
        output = output.decode('windows-1252')
        
        #Only works in french and english(suposed language) - If the system is in another language, it might not detect "Destination Host Unreachable" - The d is not written because it's a capital in english a small in french.
        #Destination Host Unreachable and successful pings have the same ICMP response but a different output, including a string that says "Destination Host Unreachable" (in english).
        if "estination" in output:
            print('The router cannot be ping. Destination Host Unreachable')
            return True
        
        #Correct - Ping is working
        return False

    #Request Timed Out raises an error.
    except subprocess.CalledProcessError:
        print('The router cannot be ping. Request Timed Out')
        return True
    

def validate_OS(osInput):
    """ The function verifies if the value entered is either '1', '2' or '3'.

    Args:
        osInput (string): This string should be '1', '2' or '3'. It is the value of the operating system of the router. 1: Cisco IOS, 2: VyOS, 3: Mikrotik RouterOS

    Returns:
        boolean: If the argument is a string with a value of '1', '2' or '3', it returns False. Otherwise, it returns True.
    """
    try:
        if not (int(osInput) >= 1 and int(osInput) <= 3):
            print('The OS number has been written incorrectly. Please type 1 (CSR), 2 (VyOS) or 3 (Mikrotik)')
            return True
        
        return False
    except ValueError:
        print('The OS number has been written incorrectly. Please type 1 (CSR), 2 (VyOS) or 3 (Mikrotik)')
        return True


def add_route(targetIPMask, mainLeftOS, nextHop, distance='0'):
    """ This function produces a command to add a new route on the router. It has to work for the 3 differents operating systems.

    Args:
        targetIPMask (string): The target value is a string with an IP adress and its subnet mask. It is an IP of the network that should be reachable by adding this route command.
        mainLeftOS (string): The operating system of the router on which the route is being added. It is equal to 1 (CSR), 2 (VyOS) or 3 (Mikrotik)
        nextHop (string): This is next hop of the router on which the route is being added to reach the targeted network.
        distance (str, optional): If the new route is a back-up route, this argument is equal to 5 in order to have a floating static route. Defaults to '1'.

    Returns:
        string: String that adds a route
    """

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

    targetNetwork = get_network(targetIPMask)
    targetMask = traduction_subnet_mask[targetIPMask.split('/')[1]]
    targetNetworkMask = targetNetwork + '/' + targetIPMask.split('/')[1]
    

    #CSR
    if mainLeftOS == '1':
        new_route = 'ip route ' + targetNetwork + ' ' + targetMask + ' ' + nextHop + ' ' + distance

    #VyOS
    elif mainLeftOS == '2':
        new_route = 'set protocols static route ' + targetNetworkMask + ' next-hop ' + nextHop + ' distance \'' + distance + '\''

    #Mikrotik
    elif mainLeftOS == '3':
        new_route = 'ip route add dst-address=' + targetNetworkMask + ' gateway=' + nextHop + ' distance=' + distance
    
    return new_route


def validate_positive_integer(stringNumber):
    """This function verifies if the integer (in a string format) is a positive integer.

    Args:
        stringNumber (string): String input

    Returns:
        boolean: If the argument is a string with a value of a positive integer, it returns False. Otherwise, it returns True.
    """
    try:
        if not int(stringNumber) > 0:
                print('The input has to be a positive integer')
                return True

    except ValueError:
        print("The input is not an integer. Try again.")
        return True
    


def get_config(routers, router):
    """After all the values for the configuration have been entered, this function is called to produce the configuration of the 4 routers.

    Args:
        routers (list): This list contains the 4 Router objects with the values of the 4 routers
        router (int): This integer is an index for the "routers" list.

    Returns:
        list: The return value is a list of strings. Each string is command to execute on the router. The whole list is the configuration to implement on one router.
    """
    if router == 1:
        selector = 0
        otherRouter = 1
        otherBackupRouter = 3
    elif router == 2:
        selector = 1
        otherRouter = 0
        otherBackupRouter = 2
    elif router == 3:
        selector = 2
        otherRouter = 1
        otherBackupRouter = 3
    elif router == 4:
        selector = 3
        otherRouter = 0
        otherBackupRouter = 2

    if routers[selector].mainTunnel.leftRouter == routers[selector]:
        mainPrivateIP = routers[selector].mainTunnel.leftPrivateIP
    elif routers[selector].mainTunnel.rightRouter == routers[selector]:
        mainPrivateIP = routers[selector].mainTunnel.rightPrivateIP

    if routers[selector].backupTunnel.leftRouter == routers[selector]:
        backupPrivateIP = routers[selector].backupTunnel.leftPrivateIP
    elif routers[selector].backupTunnel.rightRouter == routers[selector]:
        backupPrivateIP = routers[selector].backupTunnel.rightPrivateIP

    config = []


    #CSR
    if routers[selector].operatingSystem == '1':
        config = [
            'configure terminal', routers[selector].mainRoute, 
            routers[selector].backupRoute, routers[selector].mainGRERoute,
            routers[selector].backupGRERoute,
            'interface tunnel ' + routers[selector].mainTunnel.name, 
            'ip mtu ' +  routers[selector].mainTunnel.mtu, 
            'ip tcp adjust-mss ' +  routers[selector].mainTunnel.mss,
            'ip address ' + mainPrivateIP.split('/')[0] + ' 255.255.255.252',
            'tunnel source ' + routers[selector].insidePublicIP.split('/')[0], 
            'tunnel destination ' + routers[otherRouter].insidePublicIP.split('/')[0],
            'keepalive ' + routers[selector].mainTunnel.keepAlive, 
            'interface tunnel ' + routers[selector].backupTunnel.name,
            'ip mtu ' +  routers[selector].backupTunnel.mtu, 
            'ip tcp adjust-mss ' +  routers[selector].backupTunnel.mss,
            'ip address ' + backupPrivateIP.split('/')[0] + ' 255.255.255.252',
            'tunnel source ' + routers[selector].insidePublicIP.split('/')[0], 
            'tunnel destination ' + routers[otherBackupRouter].insidePublicIP.split('/')[0],
            'keepalive ' + routers[selector].backupTunnel.keepAlive,
            'wr'
            ]

    #VyOS
    elif routers[selector].operatingSystem == '2':
        config = [
            'configure', routers[selector].mainRoute, routers[selector].backupRoute,
            routers[selector].mainGRERoute, routers[selector].backupGRERoute,
            'set interfaces tunnel ' + routers[selector].mainTunnel.name + ' address ' + mainPrivateIP,
            'set interfaces tunnel ' + routers[selector].mainTunnel.name + ' encapsulation gre',
            'set interfaces tunnel ' + routers[selector].mainTunnel.name + ' mtu ' + routers[selector].mainTunnel.mtu,
            'set firewall options ' + routers[selector].mainTunnel.name + ' adjust-mss ' + routers[selector].mainTunnel.mss,
            'set interfaces tunnel ' + routers[selector].mainTunnel.name + ' local-ip ' + routers[selector].insidePublicIP.split('/')[0],
            'set interfaces tunnel ' + routers[selector].mainTunnel.name + ' remote-ip ' + routers[otherRouter].insidePublicIP.split('/')[0],
            'set interfaces tunnel ' + routers[selector].backupTunnel.name + ' address ' + backupPrivateIP,
            'set interfaces tunnel ' + routers[selector].backupTunnel.name + ' encapsulation gre',
            'set interfaces tunnel ' + routers[selector].backupTunnel.name + ' mtu ' + routers[selector].backupTunnel.mtu,
            'set firewall options ' + routers[selector].backupTunnel.name + ' adjust-mss ' + routers[selector].backupTunnel.mss,
            'set interfaces tunnel ' + routers[selector].backupTunnel.name + ' local-ip ' + routers[otherBackupRouter].insidePublicIP.split('/')[0],
            'set interfaces tunnel ' + routers[selector].backupTunnel.name + ' remote-ip ' + routers[selector].backupTunnel.keepAlive,
            'commit', 'save'
            ]       

    #Mikrotik
    elif routers[selector].operatingSystem == '3':
        config = [
            routers[selector].mainRoute, routers[selector].backupRoute,
            routers[selector].mainGRERoute, routers[selector].backupGRERoute,
            '/interface gre add name=' + routers[selector].mainTunnel.name + ' remote-address=' + routers[otherRouter].insidePublicIP.split('/')[0] + ' local-address=' + routers[selector].insidePublicIP.split('/')[0],
            '/interface gre set name=' + routers[selector].mainTunnel.name + ' mtu=' + routers[selector].mainTunnel.mtu,
            '/ip firewall mangle add out-interface=' + routers[selector].mainTunnel.name + ' protocol=tcp tcp-flags=syn action=change-mss new-mss=' + routers[selector].mainTunnel.mss + ' chain=forward tcp-mss=' + str(int(routers[selector].mainTunnel.mss) + 1)  + '-65535',
            '/ip address  add address=' + mainPrivateIP + ' interface=' + routers[selector].mainTunnel.name,
            '/interface gre add name=' + routers[selector].backupTunnel.name + ' remote-address=' + routers[otherBackupRouter].insidePublicIP.split('/')[0] + ' local-address=' + routers[selector].insidePublicIP.split('/')[0],
            '/interface gre set name=' + routers[selector].backupTunnel.name + ' mtu=' + routers[selector].backupTunnel.mtu,
            '/ip firewall mangle add out-interface=' + routers[selector].backupTunnel.name + ' protocol=tcp tcp-flags=syn action=change-mss new-mss=' + routers[selector].backupTunnel.mss + ' chain=forward tcp-mss=' + str(int(routers[selector].backupTunnel.mss) + 1) +'-65535',
            '/ip address  add address=' + backupPrivateIP + ' interface=' + routers[selector].backupTunnel.name
        ]
            

    return config


def is_in_network(oldIP, newIP):
    """This function verifies if two IP address are in the same network.

    Args:
        oldIP (string): The oldIP is a string with an IP adress and its subnet mask.
        newIP (string): The newIP value is a string with an IP adress and its subnet mask.

    Returns:
        boolean: If the newIP is in the same network has the oldIP, it returns False. Otherwise, it returns True.
    """    

    #Verfies if the two subnet masks are equal
    if not oldIP.split('/')[1] == newIP.split('/')[1]:
        print('The input mask does not match with the subnet.')
        return True

    oldNetwork = get_network(oldIP)
    newNetwork = get_network(newIP)
    

    if not oldNetwork == newNetwork:
        print('The input IP is not on the right subnet.')
        return True

    return False


def get_network(IPMask):
    """It gets the network address of the network based on an IP address of this network.

    Args:
        IPMask (string): The IPMask is a string with an IP adress and its subnet mask.

    Returns:
        string: The return value is the network of IPMask. Without the mask.
    """

    IPSplit = IPMask.split('/')[0].split('.')
    numberHostBytes = 32 - int(IPMask.split('/')[1])
    binaryIP = [str(bin(int(IPSplit[0])))[2:], str(bin(int(IPSplit[1])))[2:], str(bin(int(IPSplit[2])))[2:], str(bin(int(IPSplit[3])))[2:]]
    
    for classIP in range(len(binaryIP)):
        while len(binaryIP[classIP]) < 8:
            binaryIP[classIP] = '0' + binaryIP[classIP]

    binaryIP = ''.join(binaryIP)
    binaryNetwork = binaryIP[:len(binaryIP) - numberHostBytes]

    while len(binaryNetwork) < 32:
            binaryNetwork = binaryNetwork + '0'

    binaryNetworkSplit = ['', '', '', '']

    classIP = 0
    for byte in range(len(binaryNetwork)):
        byte += 1
        binaryNetworkSplit[classIP] += binaryNetwork[byte-1]
        if byte % 8 == 0 and byte > 0:
            classIP += 1

    networkSplit = ['', '', '', '']

    for classIP in range(4):
        networkSplit[classIP] += str(int(binaryNetworkSplit[classIP], 2))

    network = '.'.join(networkSplit)

    return network


def push_config(configs):
    """Pushes the configuration to the routers by using the ConnectHandler() function of the netmiko library

    Args:
        configs (list): Contains 4 list that represents the 4 configurations to push

    Returns:
        boolean: If the connection fails, it returns False. It the connection is successful, it does not return anything.
    """

    for config in range(len(configs)):
        if configs[config][0].operatingSystem == '1':
            device = {
            'ip': configs[config][0].insidePublicIP.split('/')[0],
            'device_type': "cisco_ios",
            'username': configs[config][0].username,
            'password': configs[config][0].password,
            'secret': configs[config][0].enable
        }
        elif configs[config][0].operatingSystem == '2':
            device = {
            'ip': configs[config][0].insidePublicIP.split('/')[0],
            'device_type': "vyos",
            'username': configs[config][0].username,
            'password': configs[config][0].password,
        }
        else:
            device = {
            'ip': configs[config][0].insidePublicIP.split('/')[0],
            'device_type': "mikrotik_routeros",
            'username': configs[config][0].username,
            'password': configs[config][0].password,
        }


        #Try to connect to the router
        try:
            #Opening of the connection
            connection = netmiko.ConnectHandler(**device)

            connection.enable()

            #The commands are being executed and the messages are printed
            connection.send_config_set(configs[config][1])

            #Closing of the connection
            connection.disconnect()

            print('The configuration have been pushed.')
        except:
            #Unable to connect to the router
            print('The connection to the router is impossible.')
            return False


if __name__ == '__main__':
    main()