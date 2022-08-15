# Baptiste Bemelmans - GRECA: Generic Routing Encapsulation Configuration Assistant - For SatADSL
from posixpath import split
import netmiko
import subprocess
import router


def main():
    allIP = []
    for turn in range(4):
        #Public IP of the routers
        if turn == 0:
            print('Informations about the main left router')
        elif turn == 1:
            print('Informations about the main right router')
        elif turn == 2:
            print('Informations about the back-up left router')
        elif turn == 3:
            print('Informations about the back-up right router')

        while True:
            again = False

            publicIPMask = input("Enter the public IP/mask of the router: ")

            #Validate the format of the public IP
            again = validate_IP(publicIPMask)

            """
            #Ping the first router
            if not again:
                again = ping(publicIP)"""

            if publicIPMask in allIP:
                print('This IP has already been entered.') 
                again = True

            if not again:
                allIP.append(publicIPMask)
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
            mainLeftPublicIPMask = publicIPMask
            mainLeftOS = OS

        elif turn == 1:
            mainRightPublicIPMask = publicIPMask
            mainRightOS = OS

        elif turn == 2:
            backupLeftPublicIPMask = publicIPMask
            backupLeftOS = OS

        elif turn == 3:
            backupRightPublicIPMask = publicIPMask
            backupRightOS = OS

    

    #Adding routes
    for turn in range(4):

        if turn == 0:
            routerSelector = "main left"
            router = mainLeftPublicIPMask
        elif turn == 1:
            routerSelector = "main right"
            router = mainRightPublicIPMask
        elif turn == 2:
            routerSelector = "back-up left"
            router = backupLeftPublicIPMask
        elif turn == 3:
            routerSelector = "back-up right"
            router = backupRightPublicIPMask


        while True:
            again = False
                
            nextHop = input("Next hop for the " + routerSelector + " router : ")

            again = validate_IP(nextHop)

            again = is_in_network(router, nextHop)

            if nextHop in allIP :
                print('This IP has already been entered.') 
                again = True


            if not again:
                allIP.append(nextHop)
                break
        
        
        if not again and turn == 0:
            mainLeftRouterMainRoute = add_route(mainRightPublicIPMask, mainLeftOS, nextHop)
            mainLeftRouterBackupRoute = add_route(backupRightPublicIPMask, backupLeftOS, nextHop, '5')
        
        elif not again and turn == 1:
            mainRightRouterMainRoute = add_route(mainLeftPublicIPMask, mainRightOS, nextHop)
            mainRightRouterBackupRoute = add_route(backupLeftPublicIPMask, backupRightOS, nextHop, '5')

        elif not again and turn == 2:
            backupLeftRouterMainRoute = add_route(mainRightPublicIPMask, mainLeftOS, nextHop)
            backupLeftRouterBackupRoute = add_route(backupRightPublicIPMask, backupLeftOS, nextHop, '5')

        elif not again and turn == 3:
            backupRightRouterMainRoute = add_route(mainLeftPublicIPMask, mainRightOS, nextHop)
            backupRightRouterBackupRoute = add_route(backupLeftPublicIPMask, backupRightOS, nextHop, '5')


    #Tunnels, private IPs, keep-alive
    for turn in range(4):

        if turn == 0:
            tunnelSelector = "main"
            routerSelector = "main left router"
        elif turn == 1:
            tunnelSelector = "back-up"
        elif turn == 2:
            tunnelSelector = "main"
            routerSelector = "back-up left router"
        elif turn == 3:
            tunnelSelector = "back-up"

        while True:
            #Name of the GRE tunnel
            tunnel = input("Enter the name of the " + tunnelSelector + " tunnel for the " + routerSelector + "(default name: [insert generated tunnel name]): ")

            if turn == 1:
                if tunnel == tunnel1:
                    print('This tunnel name is already used.')
                    again = True
            
            elif turn == 2:
                if tunnel == tunnel1 or tunnel == tunnel2:
                    print('This tunnel name is already used.')
                    again = True
            
            elif turn == 3:
                if tunnel == tunnel1 or tunnel == tunnel2 or tunnel == tunnel3:
                    print('This tunnel name is already used.')
                    again = True

            if ' ' in tunnel:
                print('Space are not allowed in the tunnel name.')
                again = True
            
            if not again:
                break

        while True:
            mtu = input("Enter the maximum transmission unit (MTU) for the \'" + tunnel + "\' tunnel(default value: 10194). : ")
            again = validate_positive_integer(mtu)
            if not again:
                if int(mtu) > 10194:
                    print('Maximum value is too high. It cannot exceed 10194.')
                else:
                    break


        while True:
            keepAliveTimeOut = input("Enter the number of seconds for the keep-alive for this tunnel (default time: 5(seconds)): ")
            again = validate_positive_integer(keepAliveTimeOut)
            if not again:
                break

        while True: 
            keepAliveRetries = input("Enter the number of retries for this tunnel (default number: 4): ")
            again = validate_positive_integer(keepAliveRetries)
            if not again:
                break

        privateIPs = []
        #Private IPs
        for routerTurn in range(2):
            if turn == 0:
                if routerTurn == 0:
                    routerSelector = "main left"
                elif routerTurn == 1:
                    routerSelector = "main right"
            elif turn == 1:
                if routerTurn == 0:
                    routerSelector = "main left"
                elif routerTurn == 1:
                    routerSelector = "back-up right"
            elif turn == 2:
                if routerTurn == 0:
                    routerSelector = "back-up left"
                elif routerTurn == 1:
                    routerSelector = "main right"
            elif turn == 3:
                if routerTurn == 0:
                    routerSelector = "back-up left"
                elif routerTurn == 1:
                    routerSelector = "back-up right"


            while True:
                again = False

                privateIPMask = input("Enter the private IP/mask of the " + routerSelector + " router for \'" + tunnel + "\' : ")

                #Validate the format of the private
                again = validate_IP(privateIPMask)

                if privateIPMask in privateIPs:
                    print('This private IP has already been entered.') 
                    again = True

                if turn % 2 == 1:
                    again = is_in_network(privateIPs.append(len(privateIPs - 1)), privateIPMask)

                if not again:
                    if privateIPMask.split('/')[1] == "30":
                        privateIPs.append(privateIPMask)
                        break
                    else:
                        print("The subnet mask for a tunnel has to be /30.")



        if turn == 0:
            tunnel1 = tunnel
            mtu1 = mtu
            keepAliveTimeOut1 = keepAliveTimeOut
            keepAliveRetries1 = keepAliveRetries

        elif turn == 1:
            tunnel2 = tunnel
            mtu2 = mtu
            keepAliveTimeOut2 = keepAliveTimeOut
            keepAliveRetries2 = keepAliveRetries
        
        elif turn == 2:
            tunnel3 = tunnel
            mtu3 = mtu
            keepAliveTimeOut3 = keepAliveTimeOut
            keepAliveRetries3 = keepAliveRetries
        
        elif turn == 3:
            tunnel4 = tunnel
            mtu4 = mtu
            keepAliveTimeOut4 = keepAliveTimeOut
            keepAliveRetries4 = keepAliveRetries


    values = {
        "mainLeftPublicIPMask": mainLeftPublicIPMask,
        "backupLeftPublicIPMask": backupLeftPublicIPMask,
        "mainRightPublicIPMask": mainRightPublicIPMask,
        "backupRightPublicIPMask": backupRightPublicIPMask,
        "mainLeftOS": mainLeftOS,
        "backupLeftOS": backupLeftOS,
        "mainRightOS": mainRightOS,
        "backupRightOS": backupRightOS,
        "mainLeftRouterMainRoute": mainLeftRouterMainRoute,
        "mainLeftRouterBackupRoute": mainLeftRouterBackupRoute,
        "mainRightRouterMainRoute": mainRightRouterMainRoute,
        "mainRightRouterBackupRoute": mainRightRouterBackupRoute,
        "backupLeftRouterMainRoute": backupLeftRouterMainRoute,
        "backupLeftRouterBackupRoute": backupLeftRouterBackupRoute,
        "backupRightRouterMainRoute": backupRightRouterMainRoute,
        "backupRightRouterBackupRoute": backupRightRouterBackupRoute,
        "mainLeftRouterMainPrivateIPMask": privateIPs[0],
        "mainLeftRouterBackupPrivateIPMask": privateIPs[2],
        "mainRightRouterMainPrivateIPMask": privateIPs[1],
        "mainRightRouterBackupPrivateIPMask": privateIPs[5],
        "backupLeftRouterMainPrivateIPMask": privateIPs[4],
        "backupLeftRouterBackupPrivateIPMask": privateIPs[6],
        "backupRightRouterMainPrivateIPMask": privateIPs[3],
        "backupRightRouterBackupPrivateIPMask": privateIPs[7],
        "tunnel1": tunnel1,
        "tunnel2": tunnel2,
        "tunnel3": tunnel3,
        "tunnel4": tunnel4,
        "mtu1": mtu1,
        "mtu2": mtu2,
        "mtu3": mtu3,
        "mtu4": mtu4,
        "keepAlive1": keepAliveTimeOut1 + ' ' + keepAliveRetries1,
        "keepAlive2": keepAliveTimeOut2 + ' ' + keepAliveRetries2,
        "keepAlive3": keepAliveTimeOut3 + ' ' + keepAliveRetries3,
        "keepAlive4": keepAliveTimeOut4 + ' ' + keepAliveRetries4
    }

    config_router1 = get_config(values, 1)
    config_router2 = get_config(values, 2)
    config_router3 = get_config(values, 3)
    config_router4 = get_config(values, 4)

    configs = [config_router1, config_router2, config_router3, config_router4]

    print(configs)

    stop = input("Press any key to stop")



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
    
    #The IP's are divided into classes. There must be four classes per IP
    if len(ipTestClasses) != 4:
        print('The IP has been written incorrectly. Ex: 197.164.73.5/24')
        return True

    #There must be only one part to the mask
    try:
        if len(maskTest) == 0 or not (int(maskTest) >= 1 and int(maskTest) <= 30):
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
def add_route(targetIPMask, mainLeftOS, nextHop, distance='1'):

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
    try:
        if not int(stringNumber) >= 0:
                print('The input has to be a positive integer')
                return True

    except ValueError:
        print("The input is not an integer. Try again.")
        return True
    


def get_config(values, router):
    if router == 1:
        selector = "mainLeft"
        otherRouter = "mainRight"
        otherBackupRouter = "backupRight"
        tunnel = "1"
        backupTunnel = "2"
    elif router == 2:
        selector = "backupLeft"
        otherRouter = "mainRight"
        otherBackupRouter = "backupRight"
        tunnel = "3"
        backupTunnel = "4"
    elif router == 3:
        selector = "mainRight"
        otherRouter = "mainLeft"
        otherBackupRouter = "backupLeft"
        tunnel = "1"
        backupTunnel = "3"
    elif router == 4:
        selector = "backupRight"
        otherRouter = "mainLeft"
        otherBackupRouter = "backupLeft"
        tunnel = "2"
        backupTunnel = "4"


    #CSR
    if values[selector + "OS"] == '1':
        config = [
            'enable', 'configure terminal', values[selector + "RouterMainRoute"], 
            values[selector + "RouterBackupRoute"], 'interface tunnel ' + values["tunnel" + tunnel], 
            'ip mtu ' +  values["mtu" + tunnel], 'ip tcp adjust-mss ' +  values["mtu" + tunnel] - 40,
            'ip address ' + values[selector + "RouterMainPrivateIPMask"].split('/')[0] + ' 255.255.255.252',
            'tunnel source ' + values[selector + "PublicIPMask"].split('/')[0], 
            'tunnel destination ' + values[otherRouter + "PublicIPMask"].split('/')[0],
            'keepalive ' + values["keepAlive" + tunnel], 'interface tunnel ' + values["tunnel" + backupTunnel],
            'ip mtu ' +  values["mtu" + backupTunnel], 'ip tcp adjust-mss ' +  values["mtu" + backupTunnel] - 40,
            'ip address ' + values[selector + "RouterBackupPrivateIPMask"].split('/')[0] + ' 255.255.255.252',
            'tunnel source ' + values[selector + "PublicIPMask"].split('/')[0], 
            'tunnel destination ' + values[otherRouter + "PublicIPMask"].split('/')[0],
            'keepalive ' + values["keepAlive" + backupTunnel],
            'wr'
            ]

    #VyOS
    elif values[selector + "OS"] == '2':
        config = [
            'configure', values[selector + "RouterMainRoute"], values[selector + "RouterBackupRoute"],
            'set interfaces tunnel ' + values["tunnel" + tunnel] + ' address ' + values[selector + "RouterMainPrivateIPMask"],
            'set interfaces tunnel ' + values["tunnel" + tunnel] + ' encapsulation gre',
            'set interfaces tunnel ' + values["tunnel" + tunnel] + ' mtu ' + values["mtu" + tunnel],
            'set firewall options ' + values["tunnel" + tunnel] + ' adjust-mss ' + values["mtu" + tunnel] - 40,
            'set interfaces tunnel ' + values["tunnel" + tunnel] + ' local-ip ' + values[selector + "PublicIPMask"].split('/')[0],
            'set interfaces tunnel ' + values["tunnel" + tunnel] + ' remote-ip ' + values[otherRouter + "PublicIPMask"].split('/')[0],
            'set interfaces tunnel ' + values["tunnel" + backupTunnel] + ' address ' + values[selector + "RouterBackupTunnelPrivateIPMask"],
            'set interfaces tunnel ' + values["tunnel" + backupTunnel] + ' encapsulation gre',
            'set interfaces tunnel ' + values["tunnel" + backupTunnel] + ' mtu ' + values["mtu" + backupTunnel],
            'set firewall options ' + values["tunnel" + backupTunnel] + ' adjust-mss ' + values["mtu" + backupTunnel] - 40,
            'set interfaces tunnel ' + values["tunnel" + backupTunnel] + ' local-ip ' + values[selector + "PublicIPMask"].split('/')[0],
            'set interfaces tunnel ' + values["tunnel" + backupTunnel] + ' remote-ip ' + values[otherBackupRouter + "PublicIPMask"].split('/')[0],
            'commit', 'save'
            ]       

    #Mikrotik
    elif values[selector + "OS"] == '3':
        'configure', values[selector + "RouterMainRoute"], values[selector + "RouterBackupRoute"],
        '/interface gre add name=' + values["tunnel" + tunnel] + ' remote-address=' + values[otherRouter + "PublicIPMask"].split('/')[0] + ' local-address=' + values[selector + "PublicIPMask"].split('/')[0],
        '/interface gre set name=' + values["tunnel" + tunnel] + ' mtu=' + values["mtu" + tunnel],
        '/ip firewall mangle add out-interface=' + values["tunnel" + tunnel] + ' protocol=tcp tcp-flags=syn action=change-mss new-mss=' + values["mtu" + tunnel] - 40 + ' chain=forward tcp-mss=' + + values["mtu" + tunnel] - 39 +'-65535',
        '/interface gre add name=' + values["tunnel" + backupTunnel] + ' remote-address=' + values[otherBackupRouter + "PublicIPMask"].split('/')[0] + ' local-address=' + values[selector + "PublicIPMask"].split('/')[0],
        '/interface gre set name=' + values["tunnel" + backupTunnel] + ' mtu=' + values["mtu" + backupTunnel]
        '/ip firewall mangle add out-interface=' + values["tunnel" + backupTunnel] + ' protocol=tcp tcp-flags=syn action=change-mss new-mss=' + values["mtu" + backupTunnel] - 40 + ' chain=forward tcp-mss=' + + values["mtu" + backupTunnel] - 39 +'-65535',
        

    return config


def is_in_network(oldIP, newIP):
    #same subnet mask?
    if not oldIP.split('/')[1] == newIP.split('/')[1]:
        print('The input mask does not match with the subnet.')
        return True

    #within subnet range - we don't know where does start/end the subnet but it cannot exceed a maximum distance
    numberAvailableIP = 2 ** (32 - int(oldIP.split('/')[1])) - 2


    ipMarker = oldIP.split('/')[0].split('.')
    numberMarker = 0
    for turn in range(len(ipMarker)):
        numberMarker += int(ipMarker[turn])* 256 ** abs(turn - 3)

    newIPCompare = newIP.split('/')[0].split('.')
    numberCompare = 0
    for turn in range(len(newIPCompare)):
        numberCompare += int(newIPCompare[turn])* 256 ** abs(turn - 3)

    if abs(numberMarker - numberCompare) > numberAvailableIP:
        print('The input IP is not on the right subnet.')
        return True


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
