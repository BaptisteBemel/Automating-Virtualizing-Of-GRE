from re import A
from tunnel import Tunnel


class Router:

    def __init__(self, position):
        """Generates the router's values.

        Args:
            position (string): Tells where the router is located in the 4 routers (main/back-up, left/right)
        """

        self.position = position
        self.mgmtPublicIP = ""
        self.insidePublicIP = ""
        self.insideInterface = ""
        self.outsidePublicIP = ""
        self.outsideInterface = ""
        self.operatingSystem = ""
        self.nextHop = ""
        self.mainRoute = ""
        self.backupRoute = ""
        self.mainGRERoute = ""
        self.backupGRERoute = ""
        self.mainTunnel = ""
        self.backupTunnel = ""
        self.username = ""
        self.password = ""
        self.enable = ""
        self.poolName = ""
        self.startPool = ""
        self.endPool = ""
        self.networkNat = ""
        self.config = ""

    def get_mgmtPublicIP(self):
        """Asks the user about the management IP address and its mask for a specific router and saves the value.

        Returns:
            string: Management IP address IP/Mask entered by the user.
        """

        self.mgmtPublicIP = input(
            "Enter the management IP/mask of the " + self.position + " router: ")
        return self.mgmtPublicIP

    def get_insidePublicIP(self):
        """Asks the user about the inside public address and its mask for a specific router and saves the value.

        Returns:
            string: Inside public IP/Mask entered by the user.
        """

        self.insidePublicIP = input(
            "Enter the inside public IP/mask of the " + self.position + " router: ")
        return self.insidePublicIP

    def get_insideInterface(self):
        """Asks the user about the inside interface for a specific router and saves the value.

        Returns:
            string: Inside interface entered by the user.
        """
        self.insideInterface = input(
            "Enter the inside interface of the " + self.position + " router: ")
        return self.insideInterface

    def get_OS(self):
        """Asks the user about the operating system for a specific router and saves the value.

        Returns:
            string: Operating system entered by the user.
        """

        self.operatingSystem = input(
            "Enter the OS of the " + self.position + "  router ('1': CSR, '2': VyOS, '3': Mikrotik): ")
        return self.operatingSystem

    def get_outsidePublicIP(self):
        """Asks the user about the outside public address and its mask for a specific router and saves the value.

        Returns:
            string: Outside public IP/Mask entered by the user.
        """

        self.outsidePublicIP = input(
            "Enter the outside public IP/mask of the " + self.position + " router: ")
        return self.outsidePublicIP

    def get_outsideInterface(self):
        """Asks the user about the outside interface for a specific router and saves the value.

        Returns:
            string: Outside interface entered by the user.
        """
        self.outsideInterface = input(
            "Enter the outside interface of the " + self.position + " router: ")
        return self.outsideInterface

    def get_nextHop(self):
        """Asks the user about the next hop for a specific router and saves the value.

        Returns:
            string: Next hop entered by the user.
        """

        self.nextHop = input("Next hop for the " + self.position + " router: ")
        return self.nextHop

    def get_username(self):
        """Asks the user about the username for a specific route and saves the value.

        Returns:
            string: Username entered by the user.
        """

        self.username = input(
            "Enter the username of the " + self.position + " router: ")
        return self.username

    def get_password(self):
        """Asks the user about the password for a specific route and saves the value.

        Returns:
            string: Password entered by the user.
        """

        self.password = input(
            "Enter the password of the " + self.position + " router: ")
        return self.password

    def get_enable(self):
        """Asks the user about the enable password for a specific route and saves the value.

        Returns:
            string: Enable password entered by the user.
        """

        self.enable = input(
            "Enter the enable password of the " + self.position + " router: ")
        return self.enable

    def get_poolName(self):
        """Asks the user about the name of the pool for the NAT and saves the value.

        Returns:
            string: Name of the pool entered by the user.
        """

        self.poolName = input(
            "Enter the name of the pool for the NAT: ")
        return self.poolName

    def get_startPool(self):
        """Asks the user about the first IP address of the pool for the NAT and saves the value.

        Returns:
            string: First IP address of the pool entered by the user.
        """

        self.startPool = input(
            "Enter the first IP address of the pool for the NAT (Without the subnet mask 'x.x.x.x'): ")
        return self.startPool

    def get_endPool(self):
        """Asks the user about the last IP address of the pool for the NAT and saves the value.

        Returns:
            string: Last IP address of the pool entered by the user.
        """

        self.endPool = input(
            "Enter the last IP address of the pool for the NAT (Without the subnet mask 'x.x.x.x'): ")
        return self.endPool

    def get_networkNat(self):
        """Asks the user about the network/mask used for the NAT and saves the value.

        Returns:
            string: Network/mask for the NAT entered by the user.
        """
        self.networkNat = input(
            "Enter the network address of the pool for the NAT (With the subnet mask 'x.x.x.x/y'): ")
        return self.endPool

    def print(self):
        """ Prints the configuration for a specific router
        """

        output = "\nConfiguration of the " + self.position + " router:\nInside public IP: " + \
            self.insidePublicIP + "\nOutside public IP: " + self.outsidePublicIP + "\nOperating system: " + \
            self.operatingSystem + "\nNext hop: " + self.nextHop + "\nMain route: " + self.mainRoute + \
            "\nBack-up route: " + self.backupRoute + "\nMain GRE route: " + \
            self.mainGRERoute + "\nBack-up GRE route: " + self.backupGRERoute + \
            "\nMain tunnel: " + self.mainTunnel.name + "\nBack-up tunnel: " + self.backupTunnel.name + "\nUsername: " + \
            self.username + "\nPassword: " + self.password + \
            "\nEnable password (field empty is the router is not running on cisco IOS or if it is not enabled): " + self.enable + \
            "\nManagement IP: " + self.mgmtPublicIP + "\nInside interface: " + self.insideInterface + \
            "\nOutside interface: " + self.outsideInterface

        if self.position == "main right" or self.position == "back-up right":    
            natOutput = "\nPool name: " + self.poolName + "\nFirst IP address of the pool: " + \
                self.startPool + "\nLast IP address of the pool: " + \
                self.endPool + "\nNetwork for the NAT: " + self.networkNat

            output += natOutput

        if self.mainTunnel.key != "":
            if self.operatingSystem == "1":
                ipsecOutput = "\nKey: " + self.mainTunnel.key + \
                "\nSet name: " + self.mainTunnel.setName + "\nMap name: " + self.mainTunnel.mapName

            if self.operatingSystem == "2":
                ipsecOutput = "\nKey: " + self.mainTunnel.key + \
                "\nIKE name: " + self.mainTunnel.ikeName + "\nESP name: " + self.mainTunnel.espName

            if self.operatingSystem == "3":
                ipsecOutput = "\nKey: " + self.mainTunnel.key + \
                "\nGroup name: " + self.mainTunnel.groupName
                

            output += ipsecOutput


        print(output)
