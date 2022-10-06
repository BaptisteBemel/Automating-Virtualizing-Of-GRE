from tunnel import Tunnel


class Router:

    def __init__(self, position):
        """Generates the router's values.

        Args:
            position (string): Tells where the router is located in the 4 routers (main/back-up, left/right)
        """

        self.position = position
        self.insidePublicIP = ""
        self.outsidePublicIP = ""
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
        self.config = ""

    def get_insidePublicIP(self):
        """Asks the user about the inside public address and its mask for a specific router and saves the value.

        Returns:
            string: Inside public IP/Mask entered by the user.
        """

        self.insidePublicIP = input(
            "Enter the inside public IP/mask of the " + self.position + " router: ")
        return self.insidePublicIP

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

    def print(self):
        """ Prints the configuration for a specific router
        """

        output = "Configuration of the " + self.position + ":\nInside public IP: " + \
            self.insidePublicIP + "\nOutside public IP: " + self.outsidePublicIP + "\nOperating system: " + \
            self.operatingSystem + "\nNext hop: " + self.nextHop + "\nMain route: " + self.mainRoute + \
            "\nBack-up route: " + self.backupRoute + "\nMain GRE route: " + \
            self.mainGRERoute + "\nBack-up GRE route: " + self.backupGRERoute + \
            "\nMain tunnel: " + self.mainTunnel.name + "\nBack-up tunnel: " + self.backupTunnel.name + "\nUsername: " + \
            self.username + "\nPassword: " + self.password + \
            "\nEnable password (field empty is the router is not running on cisco IOS):" + self.enable

        print(output)
