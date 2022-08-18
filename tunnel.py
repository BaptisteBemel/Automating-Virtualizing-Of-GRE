class Tunnel:

    def __init__(self, leftPosition, leftRouter, rightPosition, rightRouter):
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

    def get_name(self):
        self.name = input("Enter the name of the " + self.leftPosition + " tunnel for the " + self.rightPosition + " (default name: [insert generated tunnel name]): ")
        return self.name

    def get_mtu(self):
        self.mtu = input("Enter the maximum transmission unit (MTU) for the \'" + self.name + "\' tunnel(default value: 1476): ")
        try:
            self.mss = str(int(self.mtu) - 40)
        except ValueError:
            pass
        return self.mtu

    def get_keepAliveTimeOut(self):
        self.keepAliveTimeOut = input("Enter the number of seconds for the keep-alive for this tunnel (default time: 5(seconds)): ")
        return self.keepAliveTimeOut

    def get_keepAliveRetries(self):
        self.keepAliveRetries = input("Enter the number of retries for this tunnel (default number: 4): ")
        self.keepAlive = self.keepAliveTimeOut + ' ' + self.keepAliveRetries
        return self.keepAliveRetries

    def get_privateIP(self, selector):
        if selector == "left":
            self.leftPrivateIP = input("Enter the private IP/mask of the left router for \'" + self.name + "\' : ")
            return self.leftPrivateIP
        else:
            self.rightPrivateIP = input("Enter the private IP/mask of the right router for \'" + self.name + "\' : ")
            return self.rightPrivateIP