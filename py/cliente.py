# Laboratorio 3.2 INFRACOM
# LUIS MIGUEL GOMEZ LONDONO, JUAN ANTONIO RESTREPO KUNZEL, JULIAN DAVID MENDOZA RUIZ

import socket
import select

serverAddressPort = ("0.0.0.0", 20001)
bufferSize = 1024
timeout = 3

# Creamos el socket UDP para la parte del cliente
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocket.bind(serverAddressPort)

while True:
    data, addr = UDPClientSocket.recvfrom(bufferSize)
    if data:
        print("Filename: {}".format(data))
        filename = data.strip()
    with open(filename, 'wb') as f:
        while True:
            ready = select.select([UDPClientSocket], [], [], timeout)
            if ready[0]:
                data, addr = UDPClientSocket.recvfrom(bufferSize)
                f.write(data)
            else:
                print("%s Finish!" % filename)
                f.close()
                break

UDPClientSocket.close()