# GRE Configuration Assistant

This project has been for the company SatADSL and for my graduation work at EPHEC.

## Installation manual:

For the correct operation of this application it is necessary to have installed, on the computer where the application will be used, Python with a version of at least 3.7 and the following Python libraries: "netmiko", "subprocess", "re", and "posixpath". 

Linux:
´(sudo) apt-get install python3´
´(sudo) apt install python3-pip´
´pip install netmiko´
´pip install regex´

The "subprocess" and "posixpath" libraries should be installed with Python.

The ping tool should also be installed. If this is not the case:

´(sudo) apt install iputils-ping´

Moreover, it is necessary that all interfaces of routers, gateways and end devices are configured beforehand. The routers on which the configurations will be applied and the end devices must be reachable by the computer on which the software is used.

It is assumed that the operating system of the computer on which the script is used is "Debian 10". If the program is used on a device with "Windows" operating system, the script must have the authorization to perform the "ping -c" command, which may require certain rights.

To install the project:
git clone https://github.com/BaptisteBemel/Automating-Virtualizing-Of-GRE.git

Once the project is installed, go to the project directory and execute the file "greca.py" with the following command:
python3 .\greca.py

## Documentation

Please find the documentation in the files. 

Here is the network diagram on which the project is based:

![arch](https://user-images.githubusercontent.com/63234160/186002472-ea36f46d-9293-48d4-b0d8-84e7d17719a2.png)
