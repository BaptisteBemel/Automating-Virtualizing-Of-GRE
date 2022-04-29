# Baptiste Bemelmans - Task for SataADSL: Write a static route based on two inputs(Customer_IP_Address/Subnet_mask, Customer_Default_Gateway_IP_Address)
# Example of usage: ./Networking_Script 197.164.73.5/24 197.164.72.2
import sys
import netmiko

def main():
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

    #The script must take two inputs. No more, no less
    if len(sys.argv) != 3:
        print('The script must take two inputs. You have entered more or less than two. Ex: ./Networking_Script 197.164.73.5/24 197.164.72.2')
        return False

    #The first input contains both the customer IP and the subnet mask. This input has to be divided based on the slash.
    input1 = sys.argv[1].split('/')

    #The first input cannot take more than a slash
    if len(input1) != 2:
        print('The first input was written incorrectly. The subnet mask has to be written with a slash. Ex: ./Networking_Script 197.164.73.5/24 197.164.72.2')
        return False

    #Function to test the IP and the IP of the gateway
    def is_ip(ip_test, is_gateway=False, translation_to_network_add=False):
        ip_test_classes = ip_test.split('.')
        customer_network_address = ''
        issue = False
        
        #The IP's are divided into classes. There must to four classes per IP
        if len(ip_test_classes) != 4:
            print('The IP, the IP of the gateway or both were written incorrectly. Ex: ./Networking_Script 197.164.73.5/24 197.164.72.2')
            issue = True

        for ip_class in range(len(ip_test_classes)):
            try:
                #The classes must be numbers between 0 and 255
                if not (int(ip_test_classes[ip_class]) >= 0 and int(ip_test_classes[ip_class]) <= 255):
                    print('The IP, the IP of the gateway or both were written incorrectly. Ex: ./Networking_Script 197.164.73.5/24 197.164.72.2')
                    issue = True
                #Forbids useless "0"
                elif len(ip_test_classes[ip_class]) > 1 and ip_test_classes[ip_class][0] == '0':
                    print('The IP, the IP of the gateway or both were written incorrectly. Useless "0" must be removed. Ex: ./Networking_Script 197.164.73.5/24 197.164.72.2')
                    issue = True
                else:
                    #The gateway cannot finish by 0
                    if is_gateway and ip_class == 3 and int(ip_test_classes[ip_class]) == 0:
                        print('The gateway cannot finish by 0')
                        issue = True
                    
                    #The customer IP cannot finish by 0
                    elif (not is_gateway) and ip_class == 3 and int(ip_test_classes[ip_class]) == 0:
                        print('The customer IP cannot finish by 0')
                        issue = True
                    
                    #Translates the customer IP to the customer network IP
                    elif (not is_gateway) and ip_class == 3 and int(ip_test_classes[ip_class]) != 0:
                        customer_network_address += '0'

                    #Creates the network address
                    else:
                        customer_network_address += ip_test_classes[ip_class] + '.'
            except:
                print('The IP, the IP of the gateway or both were written incorrectly. Ex: ./Networking_Script 197.164.73.5/24 197.164.72.2')
                issue = True

        if translation_to_network_add:
            return customer_network_address

        return issue

    #Creation the differents variables
    customer_ip_address = input1[0]
    subnet_mask = ''
    customer_default_gateway_ip_address = sys.argv[2]
    customer_network_address = ''
    
    #Check if the subnet mask is right. If it is, the subnet mask is translated
    try:
        subnet_mask = traduction_subnet_mask[input1[1]]
    except:
        print('The first input was written incorrectly or the subnet mask does not exist. Ex: ./Networking_Script 197.164.73.5/24 197.164.72.2')
        return False

    #Test if the IP and the IP of the gateway are correctly written
    if is_ip(customer_ip_address) or is_ip(customer_default_gateway_ip_address, True):
        return False

    #Get the network address of the customer
    customer_network_address = is_ip(customer_ip_address, False, True)

    #Write and print the static route
    new_route = 'ip route ' + customer_network_address + ' ' + subnet_mask + ' ' + customer_default_gateway_ip_address
    print(new_route)
    
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
        #testcommit

if __name__ == '__main__':
    main()