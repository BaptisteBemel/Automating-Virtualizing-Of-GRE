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

    print('GRE Configuration Assistant \n\n')

    for turn in range(4):
        #Management IP of the routers
        while True:
            again = False

            mgmtIPMask = routers[turn].get_mgmtPublicIP()

            #Validate the format of the management IP
            #again = validate_IP(mgmtIPMask)

            if mgmtIPMask in allIP:
                print('This IP has already been entered.') 
                again = True

            if not again:
                #again = ping(mgmtIPMask)
                pass

            if not again:
                allIP.append(mgmtIPMask)
                break

        #OS of the routers
        while True:
            again = False
  
            OS = routers[turn].get_OS() 

            #Validate the format of the public IP
            again = validate_OS(OS)

            if not again:
                break

        #Public inside IP of the routers
        while True:
            again = False

            publicIPMask = routers[turn].get_insidePublicIP()

            #Validate the format of the public IP
            again = validate_IP(publicIPMask)

            if publicIPMask in allIP:
                print('This IP has already been entered.') 
                again = True

            if not again:
                allIP.append(publicIPMask)
                break

        interfaces = []
        #Inside interface
        while True:
            again = False

            insideInterface = routers[turn].get_insideInterface()

            if insideInterface in interfaces:
                print('This interface has already been entered.') 
                again = True

            if not again:
                interfaces.append(insideInterface)
                break


        #Outside IP
        while True:
            again = False
  
            outsidePublicIP = routers[turn].get_outsidePublicIP() 

            #Validate the format of the public IP
            again = validate_IP(outsidePublicIP)

            if outsidePublicIP in allIP:
                print('This IP has already been entered.') 
                again = True

            if not again:
                break

        #Outside interface
        while True:
            again = False

            outsideInterface = routers[turn].get_outsideInterface()

            if outsideInterface in interfaces:
                print('This interface has already been entered.') 
                again = True

            if not again:
                interfaces.append(outsideInterface)
                break
        
        #NAT information
        if turn == 1:
            while True:
                again = False

                poolName = routers[turn].get_poolName()

                if not re.match("^[A-Za-z0-9_-]*$", poolName):
                    print("This input can only contains capital and small letters, numbers, underscore and dashes.")
                    again = True

                if not again:
                    break
            
            while True:
                again = False

                startPool = routers[turn].get_startPool()
                #This fake subnet is only used for validation purpose but not saved
                startPool += "/24"

                if not re.match("[0-9.]*[0-9]+", startPool):
                    print("This input can only contains figures and dots. It shall have this format 'x.x.x.x'")
                    again = True

                if not again:
                    #again = validate_IP(startPool, True)
                    pass


                if not again:
                    break
            
            while True:
                again = False

                endPool = routers[turn].get_endPool()
                #This fake subnet is only used for validation purpose but not saved
                endPool += "/24"

                if not re.match("[0-9.]*[0-9]+", startPool):
                    print("This input can only contains figures and dots. It shall have this format 'x.x.x.x'")
                    again = True

                if not again:
                    #again = validate_IP(endPool, True)
                    pass


                if not again:
                    break
            
            while True:
                again = False

                routers[turn].get_networkNat()

                if not again:
                    break

            routers[3].poolName = routers[turn].poolName
            routers[3].startPool = routers[turn].startPool
            routers[3].endPool = routers[turn].endPool
            routers[3].networkNat = routers[turn].networkNat


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

                enableConfigured = input("Does the router have an enable secret password ? ('yes'/'no'): ")

                if enableConfigured == "yes":
                    while True:
                        again = False
            
                        enable = routers[turn].get_enable() 

                        if not re.match("^[A-Za-z0-9_-]*$", enable):
                            print("This input can only contains capital and small letters, numbers, underscore and dashes.")
                            again = True

                        if not again:
                            break

                elif enableConfigured != "no":
                    again = True

                if not again:
                        break
    

    #Adding routes
    for turn in range(4):

        while True:
            again = False
                
            nextHop = routers[turn].get_nextHop()

            again = validate_IP(nextHop)

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
    while True:
        again = False

        enableIpsec = input("Do you want to configure IPsec over GRE ? ('yes'/'no'): ")

        if enableIpsec == "yes":
            enableIpsec = True
        elif enableConfigured == "no":
            enableIpsec = False
        else:
            again = True

        if not again:
                break

    tunnel1 = Tunnel('main', router1, 'main', router2, "1")
    tunnel2 = Tunnel('backup', router1, 'main', router4, "2")
    tunnel3 = Tunnel('main', router3, 'backup', router2, "3")
    tunnel4 = Tunnel('backup', router3, 'backup', router4, "4")
    

    tunnels = [tunnel1, tunnel2, tunnel3, tunnel4]

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

            tunnel = tunnels[turn].get_name()

            if not re.match("^[0-9]*$", tunnel):
                print("This input must be a number. The output name will be that number for Cisco tunnels and 'tun'+Number for VyOS and Mikrotik.")
                again = True
            
            if tunnel in tunnels :
                print('This tunnel name has already been entered.') 
                again = True

            if not again:
                tunnels.append(tunnel)
                break


        while True:
            mtu = tunnels[turn].get_mtu()
            again = validate_positive_integer(mtu)

            if not again:
                if int(mtu) > 2000 or int(mtu) < 1000:
                    print('This value is not correct. It has to be between 1000 and 2000.')
                else:
                    break


        while True:
            keepAliveFrequency = tunnels[turn].get_keepAliveFrequency()

            again = validate_positive_integer(keepAliveFrequency)

            if not again:
                if int(keepAliveFrequency) > 5:
                    print('This value is not correct. It cannot be above 5.')
                else:
                    break


        while True: 
            keepAliveRetries = tunnels[turn].get_keepAliveRetries()

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
                    privateIPMask = tunnels[turn].get_privateIP('left')
                else:
                    privateIPMask = tunnels[turn].get_privateIP('right')

                #Validate the format of the private
                again = validate_IP(privateIPMask, True)

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


    #Routes to reach the end network via the tunnels
    for turn in range(4):
        if turn % 2 == 0:
            routers[turn].mainGRERoute = add_route(routers[1].outsidePublicIP, routers[turn].operatingSystem, routers[turn].mainTunnel.rightPrivateIP)
            routers[turn].backupGRERoute = add_route(routers[3].outsidePublicIP, routers[turn].operatingSystem, routers[turn].backupTunnel.rightPrivateIP, '5')
        else:
            routers[turn].mainGRERoute = add_route(routers[0].outsidePublicIP, routers[turn].operatingSystem, routers[turn].mainTunnel.leftPrivateIP)
            routers[turn].backupGRERoute = add_route(routers[2].outsidePublicIP, routers[turn].operatingSystem, routers[turn].backupTunnel.leftPrivateIP, '5')   

    
    #Collects information for IPsec if it's enabled
    if enableIpsec:
        key = ""
        setName = ""
        mapName = ""
        ikeName = ""
        espName = ""
        groupName = ""
        for turn in range(4):
            if tunnels[turn].leftRouter.operatingSystem == "1" or tunnels[turn].rightRouter.operatingSystem == "1":
                if key == "":
                    key = tunnels[turn].get_key()
                if setName == "":
                    setName = tunnels[turn].get_setName()
                if mapName == "":
                    mapName = tunnels[turn].get_mapName()

            if tunnels[turn].leftRouter.operatingSystem == "2" or tunnels[turn].rightRouter.operatingSystem == "2":
                if key == "":
                    key = tunnels[turn].get_key()
                if ikeName == "":
                    ikeName = tunnels[turn].get_ikeName()
                if espName == "":
                    espName = tunnels[turn].get_espName()

            if tunnels[turn].leftRouter.operatingSystem == "3" or tunnels[turn].rightRouter.operatingSystem == "3":
                if key == "":
                    key = tunnels[turn].get_key()
                if groupName == "":
                    groupName = tunnels[turn].get_groupName()
        
        for turn in range(4):
            tunnels[turn].key = key
            tunnels[turn].setName = setName
            tunnels[turn].mapName = mapName
            tunnels[turn].ikeName = ikeName
            tunnels[turn].espName = espName
            tunnels[turn].groupName = groupName


            




    configs = []

    for turn in range(4):
        routers[turn].config = get_config(routers, turn + 1, enableIpsec)
        configs.append([routers[turn], routers[turn].config])  

    #The software shall be used onto linux OS. If another OS is used, change the command below to clear the terminal
    os.system("clear")  

    router1.print()
    router2.print()
    router3.print()
    router4.print()

    while True:
            again = False
  
            confirm = input("\nDo you confirm the configurations ? ('yes'/'no'): ")

            if confirm == "yes":
                push_config(configs)
            elif confirm == "no":
                while True:
                    sureAgain = False
                    sure = input("Are you sure you want to cancel the configuration ? ('yes'/'no'): ")

                    if sure == "yes":
                        print("The configuration has been cancelled.")
                    elif sure == "no":
                        again = True
                    else:
                        sureAgain = True

                    if sureAgain:
                        print("Please enter 'yes' or 'no'")
                    else:
                        break
            else:
                print("Please enter 'yes' or 'no'")
                again = False

            if not again:
                break

    
    end = input("\nPress enter to quit.")

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

    targetNetwork = get_network(targetIPMask)
    targetMask = get_full_mask(targetIPMask.split('/')[1], False)
    targetNetworkMask = targetNetwork + '/' + targetIPMask.split('/')[1]
    

    #CSR
    if mainLeftOS == '1':
        if distance != '0':
            new_route = 'ip route ' + targetNetwork + ' ' + targetMask + ' ' + nextHop.split('/')[0] + ' ' + distance
        else:
             new_route = 'ip route ' + targetNetwork + ' ' + targetMask + ' ' + nextHop.split('/')[0]

    #VyOS
    elif mainLeftOS == '2':
        if distance != '0':
            new_route = 'set protocols static route ' + targetNetworkMask + ' next-hop ' + nextHop.split('/')[0] + ' distance \'' + distance + '\''
        else:
            new_route = 'set protocols static route ' + targetNetworkMask + ' next-hop ' + nextHop.split('/')[0]

    #Mikrotik
    elif mainLeftOS == '3':
        if distance != '0':
            new_route = 'ip route add dst-address=' + targetNetworkMask + ' gateway=' + nextHop.split('/')[0] + ' distance=' + distance
        else:
            new_route = 'ip route add dst-address=' + targetNetworkMask + ' gateway=' + nextHop.split('/')[0]
    
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
    


def get_config(routers, router, enableIpsec):
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
        #GRE
        config = [
            'configure terminal', routers[selector].mainRoute, 
            routers[selector].backupRoute, routers[selector].mainGRERoute,
            routers[selector].backupGRERoute,
            'interface tunnel ' + routers[selector].mainTunnel.name, 
            'ip mtu ' +  routers[selector].mainTunnel.mtu, 
            'ip tcp adjust-mss ' +  routers[selector].mainTunnel.mss,
            'ip address ' + mainPrivateIP.split('/')[0] + ' 255.255.255.252',
            'tunnel source ' + routers[selector].insidePublicIP.split('/')[0], 
            'tunnel destination ' + routers[otherRouter].insidePublicIP.split('/')[0]]

        if routers[selector].mainTunnel.leftRouter.operatingSystem != 2 and routers[selector].mainTunnel.rightRouter.operatingSystem != 2:
            config.append('keepalive ' + routers[selector].mainTunnel.keepAlive)
        else:
            config.append('no keepalive')

        configSuite= [     
            'interface tunnel ' + routers[selector].backupTunnel.name,
            'ip mtu ' +  routers[selector].backupTunnel.mtu, 
            'ip tcp adjust-mss ' +  routers[selector].backupTunnel.mss,
            'ip address ' + backupPrivateIP.split('/')[0] + ' 255.255.255.252',
            'tunnel source ' + routers[selector].insidePublicIP.split('/')[0], 
            'tunnel destination ' + routers[otherBackupRouter].insidePublicIP.split('/')[0]
            ]

        config += configSuite

        if routers[selector].backupTunnel.leftRouter.operatingSystem != '2' and routers[selector].backupTunnel.rightRouter.operatingSystem != '2':
            config.append('keepalive ' + routers[selector].backupTunnel.keepAlive)

        config.append('exit')

        #NAT
        if routers[selector].position == routers[selector].mainTunnel.rightRouter.position:
            natConfig = [
                'interface ' + routers[selector].outsideInterface,
                'ip nat outside', 'exit' , 'interface ' + routers[selector].insideInterface,
                'ip nat inside', 'exit',
                'access-list 1 permit ' + routers[selector].networkNat.split('/')[0] + ' ' + get_full_mask(routers[selector].networkNat.split('/')[1], True),
                'ip nat pool ' + routers[selector].poolName + ' ' + routers[selector].startPool + ' ' + routers[selector].endPool + ' netmask ' + get_full_mask(routers[selector].networkNat.split('/')[1], False),
                'ip nat inside source list 1 pool ' + routers[selector].poolName
            ]

            config += natConfig

        #IPsec
        if enableIpsec:
            ipsecConfig = [
                'crypto isakmp policy 10', 'encryption aes 128',
                'hash sha256', 'authentication pre-share', 'group 20',
                'crypto isakmp key ' + routers[selector].mainTunnel.key + ' address ' + routers[otherRouter].insidePublicIP.split('/')[0],
                'crypto ipsec transform-set ' + routers[selector].mainTunnel.setName + ' esp-aes esp-sha256-hmac',
                'access-list 100 permit ip ' + get_network(routers[otherRouter].outsidePublicIP) + ' ' 
                + get_full_mask(routers[otherRouter].outsidePublicIP.split('/')[1], True) 
                + ' ' + get_network(routers[selector].outsidePublicIP) + ' ' + get_full_mask(routers[selector].outsidePublicIP.split('/')[1], True),
                'crypto map ' + routers[selector].mainTunnel.mapName + ' 10 ipsec-isakmp',
                'set peer ' + routers[otherRouter].insidePublicIP.split('/')[0],
                'set transform-set ' + routers[selector].mainTunnel.setName,
                'match address 100', 'interface ' + routers[selector].insideInterface, 'crypto map ' + routers[selector].mainTunnel.mapName,
                'exit', 'crypto isakmp policy 10', 'encryption aes 128',
                'hash sha256', 'authentication pre-share', 'group 20',
                'crypto isakmp key ' + routers[selector].backupTunnel.key + ' address ' + routers[otherBackupRouter].insidePublicIP.split('/')[0],
                'crypto ipsec transform-set ' + routers[selector].backupTunnel.setName + ' esp-aes esp-sha256-hmac',
                'access-list 100 permit ip ' + get_network(routers[otherBackupRouter].outsidePublicIP) + ' ' 
                + get_full_mask(routers[otherBackupRouter].outsidePublicIP.split('/')[1], True) 
                + ' ' + get_network(routers[selector].outsidePublicIP) + ' ' + get_full_mask(routers[selector].outsidePublicIP.split('/')[1], True),
                'crypto map ' + routers[selector].backupTunnel.mapName + ' 10 ipsec-isakmp',
                'set peer ' + routers[otherBackupRouter].insidePublicIP.split('/')[0],
                'set transform-set ' + routers[selector].backupTunnel.setName,
                'match address 100', 'interface ' + routers[selector].insideInterface, 'crypto map ' + routers[selector].backupTunnel.mapName
            ]

            config += ipsecConfig

        config += ['end','wr']

    #VyOS
    elif routers[selector].operatingSystem == '2':
        #GRE
        config = [
            'configure', routers[selector].mainRoute, routers[selector].backupRoute,
            routers[selector].mainGRERoute, routers[selector].backupGRERoute,
            'set interfaces tunnel tun' + routers[selector].mainTunnel.name + ' address ' + mainPrivateIP,
            'set interfaces tunnel tun' + routers[selector].mainTunnel.name + ' encapsulation gre',
            'set interfaces tunnel tun' + routers[selector].mainTunnel.name + ' mtu ' + routers[selector].mainTunnel.mtu,
            'set firewall options ' + routers[selector].mainTunnel.name + ' adjust-mss ' + routers[selector].mainTunnel.mss,
            'set interfaces tunnel tun' + routers[selector].mainTunnel.name + ' local-ip ' + routers[selector].insidePublicIP.split('/')[0],
            'set interfaces tunnel tun' + routers[selector].mainTunnel.name + ' remote-ip ' + routers[otherRouter].insidePublicIP.split('/')[0],
            'set interfaces tunnel tun' + routers[selector].backupTunnel.name + ' address ' + backupPrivateIP,
            'set interfaces tunnel tun' + routers[selector].backupTunnel.name + ' encapsulation gre',
            'set interfaces tunnel tun' + routers[selector].backupTunnel.name + ' mtu ' + routers[selector].backupTunnel.mtu,
            'set firewall options ' + routers[selector].backupTunnel.name + ' adjust-mss ' + routers[selector].backupTunnel.mss,
            'set interfaces tunnel tun' + routers[selector].backupTunnel.name + ' local-ip ' + routers[otherBackupRouter].insidePublicIP.split('/')[0],
            'set interfaces tunnel tun' + routers[selector].backupTunnel.name + ' remote-ip ' + routers[selector].backupTunnel.keepAlive,
            ]

        #NAT
        if routers[selector].position == routers[selector].mainTunnel.rightRouter.position:
            natConfig = [
                'set nat source rule 20 translation address 100.64.0.1',
                'set nat source rule 30 translation address "masquerade"',
                'set nat source rule 40 translation address 100.64.0.10-100.64.0.20'
            ]

            config += natConfig

        #IPsec
        if enableIpsec:

            ipsecConfig = [
                'set vpn ipsec ipsec-interfaces interface ' + routers[selector].insideInterface,
                'set vpn ipsec ike-group ' + routers[selector].mainTunnel.ikeName + ' proposal 1 dh-group "20"',
                'set vpn ipsec ike-group ' + routers[selector].mainTunnel.ikeName + ' proposal 1 encryption "aes128"',
                'set vpn ipsec ike-group ' + routers[selector].mainTunnel.ikeName + ' proposal 1 hash "sha256"',
                'set vpn ipsec esp-group ' + routers[selector].mainTunnel.espName + ' proposal 1 encryption "aes128"',
                'set vpn ipsec esp-group ' + routers[selector].mainTunnel.espName + ' proposal 1 hash "sha256"',
                'set vpn ipsec site-to-site peer ' + routers[otherRouter].insidePublicIP.split('/')[0] + ' authentication mode pre-shared-secret',
                'set vpn ipsec site-to-site peer ' + routers[otherRouter].insidePublicIP.split('/')[0] + ' authentication pre-shared-secret ' + routers[selector].mainTunnel.key,
                'set vpn ipsec site-to-site peer ' + routers[otherRouter].insidePublicIP.split('/')[0] + ' ike-group ' + routers[selector].mainTunnel.ikeName,
                'set vpn ipsec site-to-site peer ' + routers[otherRouter].insidePublicIP.split('/')[0] + ' default-esp-group ' + routers[selector].mainTunnel.espName,
                'set vpn ipsec site-to-site peer ' + routers[otherRouter].insidePublicIP.split('/')[0] + ' local-address ' + routers[selector].insidePublicIP.split('/')[0],
                'set vpn ipsec site-to-site peer ' + routers[otherRouter].insidePublicIP.split('/')[0] + ' tunnel 1 protocol gre',
                'set vpn ipsec ipsec-interfaces interface ' + routers[selector].insideInterface,
                'set vpn ipsec ike-group ' + routers[selector].backupTunnel.ikeName + ' proposal 1 dh-group "20"',
                'set vpn ipsec ike-group ' + routers[selector].backupTunnel.ikeName + ' proposal 1 encryption "aes128"',
                'set vpn ipsec ike-group ' + routers[selector].backupTunnel.ikeName + ' proposal 1 hash "sha256"',
                'set vpn ipsec esp-group ' + routers[selector].backupTunnel.espName + ' proposal 1 encryption "aes128"',
                'set vpn ipsec esp-group ' + routers[selector].backupTunnel.espName + ' proposal 1 hash "sha256"',
                'set vpn ipsec site-to-site peer ' + routers[otherBackupRouter].insidePublicIP.split('/')[0] + ' authentication mode pre-shared-secret',
                'set vpn ipsec site-to-site peer ' + routers[otherBackupRouter].insidePublicIP.split('/')[0] + ' authentication pre-shared-secret ' + routers[selector].backupTunnel.key,
                'set vpn ipsec site-to-site peer ' + routers[otherBackupRouter].insidePublicIP.split('/')[0] + ' ike-group ' + routers[selector].backupTunnel.ikeName,
                'set vpn ipsec site-to-site peer ' + routers[otherBackupRouter].insidePublicIP.split('/')[0] + ' default-esp-group ' + routers[selector].backupTunnel.espName,
                'set vpn ipsec site-to-site peer ' + routers[otherBackupRouter].insidePublicIP.split('/')[0] + ' local-address ' + routers[selector].insidePublicIP.split('/')[0],
                'set vpn ipsec site-to-site peer ' + routers[otherBackupRouter].insidePublicIP.split('/')[0] + ' tunnel 1 protocol gre'
            ]

            config += ipsecConfig

        config += ['commit','save']

    #Mikrotik
    elif routers[selector].operatingSystem == '3':
        #GRE
        config = [
            routers[selector].mainRoute, routers[selector].backupRoute,
            routers[selector].mainGRERoute, routers[selector].backupGRERoute,
            '/interface gre add name=' + routers[selector].mainTunnel.name + ' remote-address=' + routers[otherRouter].insidePublicIP.split('/')[0] + ' local-address=' + routers[selector].insidePublicIP.split('/')[0] + \
                ' mtu=' + routers[selector].mainTunnel.mtu
                ]
                
        if routers[selector].mainTunnel.leftRouter.operatingSystem != '2' and routers[selector].mainTunnel.rightRouter.operatingSystem != '2':
            config.append('/interface gre set name=' + routers[selector].mainTunnel.name + ' keepalive=' + routers[selector].mainTunnel.keepAliveFrequency + 's,' + routers[selector].mainTunnel.keepAliveRetries)
        

        configSuite = [
            '/ip firewall mangle add out-interface=' + routers[selector].mainTunnel.name + ' protocol=tcp tcp-flags=syn action=change-mss new-mss=' + routers[selector].mainTunnel.mss + ' chain=forward tcp-mss=' + str(int(routers[selector].mainTunnel.mss) + 1)  + '-65535',
            '/ip address  add address=' + mainPrivateIP + ' interface=' + routers[selector].mainTunnel.name,
            '/interface gre add name=' + routers[selector].backupTunnel.name + ' remote-address=' + routers[otherBackupRouter].insidePublicIP.split('/')[0] + ' local-address=' + routers[selector].insidePublicIP.split('/')[0] + \
                ' mtu=' + routers[selector].backupTunnel.mtu
                ]

        config += configSuite

        if routers[selector].backupTunnel.leftRouter.operatingSystem != '2' and routers[selector].backupTunnel.rightRouter.operatingSystem != '2':
            config.append('/interface gre set name=' + routers[selector].backupTunnel.name + ' keepalive=' + routers[selector].backupTunnel.keepAliveFrequency + 's,' + routers[selector].backupTunnel.keepAliveRetries)

        configSuite = [      
            '/ip firewall mangle add out-interface=' + routers[selector].backupTunnel.name + ' protocol=tcp tcp-flags=syn action=change-mss new-mss=' + routers[selector].backupTunnel.mss + ' chain=forward tcp-mss=' + str(int(routers[selector].backupTunnel.mss) + 1) +'-65535',
            '/ip address  add address=' + backupPrivateIP + ' interface=' + routers[selector].backupTunnel.name
        ]

        config += configSuite

        #NAT
        if routers[selector].position == routers[selector].mainTunnel.rightRouter.position:
            natConfig = ['/ip firewall nat add chain=srcnat action=masquerade out-interface=Public']

            config += natConfig

        #IPsec
        if enableIpsec:
            ipsecConfig = [
                '/ip ipsec profile add dh-group=ecp384 enc-algorithm=aes-128 name=' + routers[selector].mainTunnel.groupName,
                '/ip ipsec proposal add enc-algorithms=aes-128-cbc name=' + routers[selector].mainTunnel.groupName + ' pfs-group=ecp384',
                '/ip ipsec peer add address=' + routers[otherRouter].insidePublicIP.split('/')[0] + '/32 name=' + routers[selector].mainTunnel.groupName + ' profile=' + routers[selector].mainTunnel.groupName,
                '/ip ipsec identity add peer=' + routers[selector].mainTunnel.groupName + ' secret=' + routers[selector].mainTunnel.key,
                '/ip ipsec policy add src-address=' + get_network(routers[selector].outsidePublicIP) + routers[selector].outsidePublicIP.split('/')[1] 
                + ' src-port=any dst-address=' + get_network(routers[otherRouter].outsidePublicIP) + routers[otherRouter].outsidePublicIP.split('/')[1] 
                + ' dst-port=any tunnel=yes action=encrypt proposal=' 
                + routers[selector].mainTunnel.groupName + ' peer=' + routers[selector].mainTunnel.groupName,
                '/ip firewall nat add chain=srcnat action=accept  place-before=0 src-address=' + get_network(routers[selector].outsidePublicIP) 
                + routers[selector].outsidePublicIP.split('/')[1] 
                + ' dst-address=' + get_network(routers[otherRouter].outsidePublicIP) + routers[otherRouter].outsidePublicIP.split('/')[1],
                '/ip ipsec profile add dh-group=ecp384 enc-algorithm=aes-128 name=' + routers[selector].backupTunnel.groupName,
                '/ip ipsec proposal add enc-algorithms=aes-128-cbc name=' + routers[selector].backupTunnel.groupName + ' pfs-group=ecp384',
                '/ip ipsec peer add address=' + routers[otherBackupRouter].insidePublicIP.split('/')[0] + '/32 name=' + routers[selector].backupTunnel.groupName + ' profile=' + routers[selector].mainTunnel.groupName,
                '/ip ipsec identity add peer=' + routers[selector].backupTunnel.groupName + ' secret=' + routers[selector].backupTunnel.key,
                '/ip ipsec policy add src-address=' + get_network(routers[selector].outsidePublicIP) + routers[selector].outsidePublicIP.split('/')[1] 
                + ' src-port=any dst-address=' + get_network(routers[otherBackupRouter].outsidePublicIP) + routers[otherBackupRouter].outsidePublicIP.split('/')[1] 
                + ' dst-port=any tunnel=yes action=encrypt proposal=' 
                + routers[selector].backupTunnel.groupName + ' peer=' + routers[selector].backupTunnel.groupName,
                '/ip firewall nat add chain=srcnat action=accept  place-before=0 src-address=' + get_network(routers[selector].outsidePublicIP) 
                + routers[selector].outsidePublicIP.split('/')[1] 
                + ' dst-address=' + get_network(routers[otherBackupRouter].outsidePublicIP) + routers[otherBackupRouter].outsidePublicIP.split('/')[1]
            ]

            config += ipsecConfig          

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


def get_full_mask(mask, inverted):
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

    if inverted:
        mask = traduction_subnet_mask[mask]
        classes = mask.split('.')
        newMask = []

        for classId in range(len(classes)):
            classValue = int(classes[classId])
            classValue = 255 - classValue
            classValue = str(classValue)
            newMask.append(classValue)
        
        mask = '.'.join(newMask)

    else:
        mask = traduction_subnet_mask[mask]

    return mask




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
            'ip': configs[config][0].mgmtPublicIP.split('/')[0],
            'device_type': "cisco_ios",
            'username': configs[config][0].username,
            'password': configs[config][0].password,
            'secret': configs[config][0].enable
        }
        elif configs[config][0].operatingSystem == '2':
            device = {
            'ip': configs[config][0].mgmtPublicIP.split('/')[0],
            'device_type': "vyos",
            'username': configs[config][0].username,
            'password': configs[config][0].password
        }
        else:
            device = {
            'ip': configs[config][0].mgmtPublicIP.split('/')[0],
            'device_type': "mikrotik_routeros",
            'username': configs[config][0].username,
            'password': configs[config][0].password
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

            print('A configuration has been pushed.')

        except:
            #Unable to connect to the router
            print('The connection to the router is impossible.')
            return False
    
    print('All the configurations have been pushed.')


if __name__ == '__main__':
    main()