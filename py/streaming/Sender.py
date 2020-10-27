import socket
import struct
import sys
import threading
import cv2
import time

message = "Elija el canal al que se quiere conectar. \n1. iPhone 12 \n2. WARZONE \n3. TECNOLOGIA"
lobby_multicast_group = ("224.3.29.71", 10000)

def multicastSelector(numCanal):
    switcher = {
        1: 10001,
        2: 10002,
        3: 10003
    }
    return switcher.get(int(numCanal), 10000)

def videoChannelPath(numCanal):
    switcher = {
        1: "./iphone12.mp4",
        2: "./cod.mp4",
        3: "./tec.mp4"
    }
    return switcher.get(int(numCanal))

#Definicion total para la ejecucion de un canal
def canal(numCanal):
    #print("INICIANDO CANAL %s" % numCanal)
    port = multicastSelector(numCanal)
    path = videoChannelPath(numCanal)
    new_multicast_group = ("224.3.29.71", port)
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ttl = struct.pack('b',1)
    soc.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
    #print("Empezando transmision de archivos...")
    while True:
        video = cv2.VideoCapture(path)
        while video.isOpened():
            success, image = video.read()
            if not success:
                break
            ret, jpeg = cv2.imencode('.jpeg', image)
            if not ret:
                break
            #print('Envio del canal '+str(numCanal))
            # if numCanal == 1:
            #     print('Tamaño de buffer '+str(sys.getsizeof(jpeg.tobytes())))
            if sys.getsizeof(jpeg.tobytes()) < 65535:
                soc.sendto(jpeg.tobytes(), new_multicast_group)
            time.sleep(0.05)

#Creamos un socket diagram
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Establecemos un timeout para que el socket no falle
sock.settimeout(10000)

#Establecemos un tiempo de vida para los mensajes
#Cambiar a 50 x si algo
ttl = struct.pack('b', 50)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

try:
    #Mandamos el mensaje al grupo de difusion
    print("Enviando: '%s'" % message)
    sent = sock.sendto(message.encode("ascii"), lobby_multicast_group)

    #Buscar respuestas de los recipientes
    while True:
        try:
            print("Esperando respuesta")
            data, server = sock.recvfrom(16)
            dataS = data.decode("ascii")
            if "SELECT" in dataS:
                num = dataS.split("#")[1]
                portNumEleccion = "PORT#%s"%multicastSelector(num)
                sock.sendto(portNumEleccion.encode("ascii"), lobby_multicast_group)
            threading.Thread(target = canal, args=(1,)).start()
            threading.Thread(target = canal, args=(2,)).start()
            threading.Thread(target = canal, args=(3,)).start()
        except socket.timeout:
            print("Timeout, no hay mas respuestas")
            break

finally:
    print("Socket cerrado")
    sock.close()