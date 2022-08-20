Manuel d'installation:

Pour le bon fonctionnement de cette application sont nécessaires qu'il soit installé, sur l'ordinateur sur lequel sera utilisé l'application, Python avec une version d'au moins 3.7, les bilbiothèques Python suivantes: "netmiko", "subprocess", "re", and "posixpath". 

Linux:
(sudo) apt-get install python3
(sudo) apt install python3-pip
pip install netmiko
pip install regex

Les bibliothèques "subprocess" et "posixpath" devraient être installées avec Python.

Doit aussi être installé l'outil ping. Si ce n'est pas le cas:

(sudo) apt install iputils-ping

Il est supposé que l'operating system de l'ordinateur sur lequel est utilisé le script est "Debian 10". Si le programme est utilisé sur un appareil avec pour operating system "Windows", il faut que le script aie l'autorisation pour effectuer la commande "ping -c", ce qui peut nécessité l'obtention de certains droits.

