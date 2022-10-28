class Tunnel:

    def __init__(self, leftPosition, leftRouter, rightPosition, rightRouter):
        """Generates the tunnel's value.

        Args:
            leftPosition (string): Tells where the router is located in the 4 routers (main/back-up, left/right) 
            leftRouter (Router): Router object of the left router
            rightPosition (string): Tells where the router is located in the 4 routers (main/back-up, left/right)
            rightRouter (Router): Router object of the right router
        """

        self.leftPosition = leftPosition
        self.rightPosition = rightPosition
        self.leftRouter = leftRouter
        self.rightRouter = rightRouter
        self.name = ""
        self.mtu = ""
        self.mss = ""
        self.leftPrivateIP = ""
        self.rightPrivateIP = ""
        self.keepAlive = ""
        self.keepAliveTimeOut = ""
        self.keepAliveRetries = ""
        self.typeTunnel = ""

    def get_name(self):
        """Asks the user about the name of a specific tunnel and saves the value.

        Returns:
            string: Name entered by the user.
        """

        self.name = input("Enter the name of the " + self.leftPosition + " tunnel for the " + self.rightPosition + " left router: ")
        return self.name

    def get_mtu(self):
        """Asks the user about the mtu of a specific tunnel and saves the value. It also calculates the mss based on the entered mtu.

        Returns:
            string: MTU entered by the user.
        """

        self.mtu = input("Enter the maximum transmission unit (MTU) for the \'" + self.name + "\' tunnel(default value: 1476): ")
        try:
            self.mss = str(int(self.mtu) - 40)
        except ValueError:
            pass
        return self.mtu

    def get_keepAliveTimeOut(self):
        """Asks the user about the time-out for the keep alive of a specific tunnel and saves the value.

        Returns:
            string: Keep alive time-out entered by the user.
        """

        self.keepAliveTimeOut = input("Enter the number of seconds for the keep-alive for this tunnel (default time: 5(seconds)): ")
        return self.keepAliveTimeOut

    def get_keepAliveRetries(self):
        """Asks the user about the number of retries for the keep alive of a specific tunnel and saves the value.

        Returns:
            string: Number of keep alive retries entered by the user.
        """

        self.keepAliveRetries = input("Enter the number of retries for this tunnel (default number: 4): ")
        self.keepAlive = self.keepAliveTimeOut + ' ' + self.keepAliveRetries
        return self.keepAliveRetries

    def get_privateIP(self, selector):
        """Asks the user about the private IP and its subnet mask for a specific tunnel and a specific router and saves the value.

        Args:
            selector (string): Selects if the entered private IP/Mask are for the left router or the right one.

        Returns:
            string: Private IP and its mask entered by the user.
        """

        if selector == "left":
            self.leftPrivateIP = input("Enter the private IP/mask of the left router for \'" + self.name + "\' : ")
            return self.leftPrivateIP
        else:
            self.rightPrivateIP = input("Enter the private IP/mask of the right router for \'" + self.name + "\' : ")
            return self.rightPrivateIP