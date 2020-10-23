# Laboratorio 3.2 INFRACOM
# LUIS MIGUEL GOMEZ LONDONO, JUAN ANTONIO RESTREPO KUNZEL, JULIAN DAVID MENDOZA RUIZ

# Imports ****IMPORTAR pip3 install tqdm
import socket
import time
import sys

localIP = "0.0.0.0"
localPort = 20001
bufferSize = 1024

filename = sys.argv[1]

# Creamos el datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.sendto(filename.encode(), (localIP, localPort))
print("Sending %s ..." % filename)

with open(filename, "rb") as f:
    data = f.read(bufferSize)
    while(data):
        if(UDPServerSocket.sendto(data, (localIP, localPort))):
            data = f.read(bufferSize)
            time.sleep(0.02)
    f.close()
UDPServerSocket.close()
