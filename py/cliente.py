# Laboratorio 3.2 INFRACOM
# LUIS MIGUEL GOMEZ LONDONO, JUAN ANTONIO RESTREPO KUNZEL, JULIAN DAVID MENDOZA RUIZ


import socket
import logging
import time
import hashlib

# Se inicializa el log, se le dan estas características para que lo escriba como queremos
logging.basicConfig(filename="resultados.log", level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                    )
hashMensaje=hashlib.sha256()


# la ip donde está corrriendo el servidor localhost = 127.0.0.1
host = 'localhost'
#puerto de conexión del socket. En este caso es el puerto donde corre el servidor.
port=8080

buffersize = 1024

UDPClientSocket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Se conecta al servidor
UDPClientSocket.connect((host, port))
print("listo para recibir informacion")
logging.info("CLIENTE listo para recibir la info")
UDPClientSocket.sendto("listo".encode(),(host,port))
#Se empieza a recibir informacion
num_paquetes=0
f = open("recibido.mp4", 'wb')
while True:
    data,adrr=UDPClientSocket.recvfrom(buffersize)
    start_time=time.time()
    f.write(data)
    #De contener el encabezado enviado entonces entra en el if
    if (data.__contains__(b"HASH")):
        
        print("LLEGÓ DICIEMBRE")
        
        i=data.find(b"HASH")
        hashMensaje.update(data[:i])
        hash_recibido = data[i+4:] #Se le suman 4 debido a que se emvió con HASH + mensaje esos 4 son del HASH
        print("El hash recibido es ", hash_recibido)
        print("El hash calculado es",hashMensaje.hexdigest())

        #Se revisa si el hash cuadra con el recibido del servidor
        if hashMensaje.hexdigest()== hash_recibido.decode():
            print("El hash llegó bien")
            logging.info("Hash está correcto")
            print("El numero de paquetes recibidos es de ", num_paquetes)
            break
        else:
            print("hash llegó maluco")
            logging.info("Hash incorrecto")
            print("El numero de paquetes recibidos es de ", num_paquetes)
            break

        #Si ya se terminó el mensaje entonces salga de ahí soldado
        if not data:
            break

    hashMensaje.update(data)
    num_paquetes+=1
finalTime = time.time() - start_time
logging.info("CLIENTE Tiempo de envio %s" % finalTime)
logging.info("---------------------------------------------")

UDPClientSocket.close()