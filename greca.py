# Baptiste Bemelmans - GRECA: Generic Routing Encapsulation Configuration Assistant - For SatADSL - made in August 2022
from msilib.schema import Error
import netmiko
import subprocess

def main():
    while True:
        again = False

        #Ask for the public IP of the 1st router
        firstPublicIPMask = input("Enter the public IP/mask of the first router: ")
        firstPublicIP = firstPublicIPMask.split('/')[0]

        #Validate the format of the public IP of the 1st router
        again = validate_IP(firstPublicIPMask)

        #Ping the first router
        print('Pinging...')
        again = ping(firstPublicIP)

        if not again:
            break


        #Find the OS of the 1st router


        #Ask for the public IP of the 1st router
        #secondPublicIP = input("Enter the public IP/mask of the first router: ")

        #Validate the format of the public IP of the 1st router
        #again = validate_IP(firstPublicIP)

        #Ping the first router


        #Find the OS of the 1st router




def validate_IP(ipMask):
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
    if len(maskTest) == 0 or not (int(maskTest) >= 1 and int(maskTest) <= 32):
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

    #if translation_to_network_add:
    #    return customer_network_address


def ping(host):
    try:
        output = subprocess.check_output("ping " + host, shell=True)

        #Correct - Ping is working
        return False
    except subprocess.CalledProcessError:
        print('The first router cannot be ping.')
        return True


if __name__ == '__main__':
    main()
