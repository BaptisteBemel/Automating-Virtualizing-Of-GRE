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
        self.mainGRERoute = ""
        self.backupGRERoute = ""
        self.mainTunnel = ""
        self.backupTunnel = ""
        self.username = ""
        self.password = ""
        self.enable = ""
        self.config = ""

    def get_insidePublicIP(self):
        self.insidePublicIP = input("Enter the public IP/mask of the " + self.position + " router: ")
        return self.insidePublicIP

    def get_OS(self):
        self.operatingSystem = input("Enter the OS of the " + self.position + "  router ('1': CSR, '2': VyOS, '3': Mikrotik): ")
        return self.operatingSystem

    def get_outsidePublicIP(self):
        self.outsidePublicIP = input("Enter the outside public IP/mask of the " + self.position + "  router: ")
        return self.outsidePublicIP

    def get_nextHop(self):
        self.nextHop = input("Next hop for the " + self.position + " router : ")
        return self.nextHop