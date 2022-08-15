from tunnel import Tunnel

class Router:

    def __init__(self, position):
        self.position = position
        self.insidePublicIP = ""
        self.outsidePublicIP = ""
        self.operatingSystem = ""
        self.nextHop = ""
        self.mainRoute = ""
        self.backupRoute = ""
        self.mainTunnel = Tunnel('main', position)
        self.backupTunnel = Tunnel('backup', position)
        self.config = ""

    def get_insidePublicIP(self):
        self.insidePublicIP = input("Enter the public IP/mask of the router: ")
        return self.insidePublicIP

    def get_OS(self):
        self.operatingSystem = input("Enter the OS of the router ('1': CSR, '2': VyOS, '3': Mikrotik): ")
        return self.operatingSystem

    def get_nextHop(self):
        self.nextHop = input("Next hop for the " + self.position + " router : ")
        return self.operatingSystem