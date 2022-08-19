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
        self.outsidePublicIP = input("Enter the outside public IP/mask of the " + self.position + " router: ")
        return self.outsidePublicIP

    def get_nextHop(self):
        self.nextHop = input("Next hop for the " + self.position + " router: ")
        return self.nextHop

    def get_username(self):
        self.username = input("Enter the username of the " + self.position + " router: ")
        return self.username

    def get_password(self):
        self.password = input("Enter the password of the " + self.position + " router: ")
        return self.password

    def get_enable(self):
        self.enable = input("Enter the enable password of the " + self.position + " router: ")
        return self.enable

    def print(self):
        output = "Configuration of the " + self.position + ":\nInside public IP: " + self.insidePublicIP + "\nOutside public IP: "  + self.outsidePublicIP 
        + "\nOperating system: "  + self.operatingSystem + "\nNext hop: " + self.nextHop + "\nMain route: " + self.mainRoute + "\nBack-up route: "
        + self.backupRoute + "\nMain GRE route: " + self.mainGRERoute + "\nBack-up GRE route: " + self.backupGRERoute + "\nMain tunnel: " + self.mainTunnel 
        + "\nBack-up tunnel: " + self.backupTunnel + "\nUsername: " + self.username + "\nPassword: " + self.password
        + "\nEnable password (field empty is the router is not running on cisco IOS):" + self.enable
