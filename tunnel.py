from turtle import pos


class Tunnel:

    def __init__(self, leftPosition, leftRouter, rightPosition, rightRouter, tunnelId):
        """Generates the tunnel's value.

        Args:
            leftPosition (string): Tells where the router is located in the 4 routers (main/back-up, left/right) 
            leftRouter (Router): Router object of the left router
            rightPosition (string): Tells where the router is located in the 4 routers (main/back-up, left/right)
            rightRouter (Router): Router object of the right router
        """

        #GRE values
        self.leftPosition = leftPosition
        self.rightPosition = rightPosition
        self.leftRouter = leftRouter
        self.rightRouter = rightRouter
        self.tunnelId = tunnelId
        self.name = ""
        self.mtu = ""
        self.mss = ""
        self.leftPrivateIP = ""
        self.rightPrivateIP = ""
        self.keepAlive = ""
        self.keepAliveFrequency = ""
        self.keepAliveRetries = ""

        #IPsec values
        #Global value
        self.key = ""
        #Cisco values
        self.setName = ""
        self.mapName = ""
        #VyOS values
        self.ikeName = ""
        self.espName = ""
        #Cisco and VyOS
        self.leftInsideInterface1 = ""
        self.leftInsideInterface2 = ""
        self.rightInsideInterface1 = ""
        self.rightInsideInterface2 = ""
        #Mikrotik
        self.groupName = ""


    def get_name(self):
        """Asks the user about the name of a specific tunnel and saves the value.

            Cisco only accept a number as the tunnel name where the other can have a name with letters and numbers so, only a number can be entered and for VyOS or Mikrotik this number will
            be concanate 'tun'+Number during the generation of the configuration.

        Returns:
            string: Name entered by the user.
        """

        self.name = input("Enter the name of the " + self.leftPosition + " tunnel for the " + self.rightPosition + " left router (Only use figures - Default value:" + self.tunnelId + "): ")
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

    def get_keepAliveFrequency(self):
        """Asks the user about the time-out for the keep alive of a specific tunnel and saves the value.

        Returns:
            string: Keep alive time-out entered by the user.
        """

        self.keepAliveFrequency = input("Enter the number of seconds for the keep-alive for this tunnel (default time: 5(seconds)): ")
        return self.keepAliveFrequency

    def get_keepAliveRetries(self):
        """Asks the user about the number of retries for the keep alive of a specific tunnel and saves the value.

        Returns:
            string: Number of keep alive retries entered by the user.
        """

        self.keepAliveRetries = input("Enter the number of retries for this tunnel (default number: 4): ")
        self.keepAlive = self.keepAliveFrequency + ' ' + self.keepAliveRetries
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

    def get_key(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        self.key = input("Enter the secret key for the encryption (Criteria - At least: Min length: 8chars, Capital, small caps, a figure and a special char): ")
        return self.key

    def get_setName(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        self.setName = input("Enter the name of the set: ")
        return self.setName
    
    def get_mapName(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        self.mapName = input("Enter the name of the map: ")
        return self.mapName
    
    def get_ikeName(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        self.ikeName = input("Enter the name of the IKE group: ")
        return self.ikeName
    
    def get_espName(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        self.espName = input("Enter the name of the ESP group: ")
        return self.espName

    def get_groupName(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        self.groupName = input("Enter the name that is going to be use for the IPsec on Mikrotik: ")
        return self.groupName