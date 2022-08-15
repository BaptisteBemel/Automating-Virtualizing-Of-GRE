class Tunnel:

    def __init__(self, position, routerPosition):
        self.position = position
        self.routerPosition = routerPosition
        self.name = ""
        self.mtu = ""
        self.mss = ""
        self.mainPrivateIP = ""
        self.backupPrivateIP = ""
        self.keepAlive = ""
        self.keepAliveTimeOut = ""
        self.keepAliveRetries = ""

    def get_name(self):
        self.mainTunnel = input("Enter the name of the " + self.position + " tunnel for the " + self.routerPosition + " (default name: [insert generated tunnel name]): ")
        return self.mainTunnel

    def get_mtu(self):
        self.mtu = input("Enter the maximum transmission unit (MTU) for the \'" + self.name + "\' tunnel(default value: 10194). : ")
        return self.mtu

    def get_keepAliveTimeOut(self):
        self.keepAliveTimeOut = input("Enter the number of seconds for the keep-alive for this tunnel (default time: 5(seconds)): ")
        return self.keepAliveTimeOut

    def get_keepAliveRetries(self):
        self.keepAliveRetries = input("Enter the number of retries for this tunnel (default number: 4): ")
        self.keepAlive = self.keepAliveTimeOut + ' ' + self.keepAliveRetries
        return self.keepAliveRetries