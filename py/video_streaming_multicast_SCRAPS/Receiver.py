import socket
import struct
import sys

multicast_group = "224.3.29.71"
#se pone vacio porque solo vamos a escuchar el multicast. Porque es la que tiene configurada la maquina.
server_address = ('', 10000)
newChannelPort = 10000

#Creamos el socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Bindiamos el socket al address del servidor
sock.bind(server_address)

#Le decimos al sistema operativo que agregue el socket al grupo multicast. Es decir
#Que nos vamos a suscribir a ese grupo de multicast
group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

#Loop de envios y mensajes de respuesta
i = 0

#Cuando recibamos el nuevo puerto esto se cambia a True para que laescucha del programa 
#se dedique a recibir el video y no comando por comando cual protocolo
readyRecieveVideo = False
while True:
    print("\nWaiting to receive channel info")
    data, address = sock.recvfrom(1024)
    print("Received %s from %s" % (data, address))
    dataS = data.decode("ascii")
    if "PORT" in dataS:
        newChannelPort = int(dataS.split("#")[1])
        new_server_address = ('', newChannelPort)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(new_server_address)
        group = socket.inet_aton(multicast_group)
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        readyRecieveVideo = True  
    if i == 0:
        eleccion = input("Enter selection: ")
        msgEleccion = 'SELECT#%s' % eleccion
        sock.sendto(msgEleccion.encode("ascii"), address)
        i = i + 1