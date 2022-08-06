# Baptiste Bemelmans - GRECA: Generic Routing Encapsulation Configuration Assistant - For SatADSL - made in August 2022
from msilib.schema import Error
from re import A
from urllib import response
import netmiko
import subprocess


def main():
    #Input for the 1st router
    while True:
        again = False


        #Ask for the public IP of the 1st router
        firstPublicIPMask = input("Enter the public IP/mask of the first router: ")
        firstPublicIP = firstPublicIPMask.split('/')[0]

        #Validate the format of the public IP of the 1st router
        again = validate_IP(firstPublicIPMask)


        """#Ping the first router
        if not again:
            print('Pinging...')
            again = ping(firstPublicIP)"""


        if not again:
            break


    while True:
        again = False
                
        #Ask for the OS of the 1st router
        firstOS = input("Enter the OS of the first router ('1': CSR, '2': VyOS, '3': Mikrotik): ")

        #Validate the format of the public IP of the 1st router
        again = validate_OS(firstOS)


        if not again:
            break

    #Input for the second router
    while True:
        again = False


        #Ask for the public IP of the 2nd router
        secondPublicIPMask = input("Enter the public IP/mask of the second router: ")
        secondPublicIP = secondPublicIPMask.split('/')[0]

        #Validate the format of the public IP of the 1st router
        again = validate_IP(secondPublicIPMask)


        """#Ping the first router
        if not again:
            print('Pinging...')
            again = ping(secondPublicIP)"""


        if not again:
            break


    while True:
        again = False
                
        #Ask for the OS of the 2nd router
        secondOS = input("Enter the OS of the second router ('1': CSR, '2': VyOS, '3': Mikrotik): ")

        #Validate the format of the public IP of the 1st router
        again = validate_OS(secondOS)


        if not again:
            break


    #Adding routes
    while True:
        again = False
                

        selector = input("Add a new route ? (yes/no) : ")

        if selector == "yes":
            again = True

            while True:
                routerSelectorAgain = False

                routerSelector = input("On which router ? (1/2) : ")

                if routerSelector == "1":
                    routerSelectorAgain = False
                    add_route(secondPublicIPMask, firstOS, firstPublicIP) #3rd parameter has to be gateway and not 1stpubip
                
                elif routerSelector == "2":
                    routerSelectorAgain = False

                else:
                    print("Wrong spelling. Try again.")
                    routerSelectorAgain = True

                if not routerSelectorAgain:
                    break

        elif selector =="no":
            again = False

        else:
            print("Wrong spelling. Try again.")
            again = True

        if not again:
            break


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
def add_route(targetIPMask, firstOS, nextHop):

    #CSR
    if firstOS == '1':
        cisco_route(targetIPMask, nextHop)


    #VyOS
    elif firstOS == '2':
        pass


    #Mikrotik
    elif firstOS == '3':
        pass


def cisco_route(targetIPMask, nextHop):

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
    targetNetwork = targetIPSplit[0:3]
    targetNetwork.append('0')
    juncture = '.'
    targetNetwork = juncture.join(targetNetwork)
    listNetworkMask = [targetNetwork, targetIPMask.split('/')[1]]
    juncture = '/'
    targetNetworkMask = juncture.join(listNetworkMask)


    #Write and print the static route
    new_route = 'ip route ' + targetNetworkMask + ' ' + nextHop
    print(new_route) #enleverleprint
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
