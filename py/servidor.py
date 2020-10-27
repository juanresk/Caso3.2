# Laboratorio 3.2 INFRACOM
# LUIS MIGUEL GOMEZ LONDONO, JUAN ANTONIO RESTREPO KUNZEL, JULIAN DAVID MENDOZA RUIZ

import socket
import time
from threading import Thread
import hashlib

buffersize = 1024

def main():
    #Arreglo con las conexiones que se unan al servidor
    connections = []
    #IP donde corre el servidor
    host='localhost'
    #Puerto donde corre el servidor
    port=8080
    #Configuracion del socket del servidor. Se usa datagram para UDP y enviar los archivos
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    

    #Crea el servidor
    serverSocket.bind((host,port))

    print("El servidor esta escuchando en el puerto %d" %port)
    texto=int (input("\n Cual video quiere mandar?"
                     "\n 1. Etee es sech"
                     "\n 2. Drake y josh"
                     "\n"))
    if texto==1:
        efe="esteessech.mp4"
    else:
        efe="actualidad.mp4"
    global file
    file=efe
    print("Archivo seleccionado: ",file)
    numerocon= int( input('\n A cuantos clientes quiere enviar el archivo?' ))

    print("Esperando conexiones")
    cont=0
    while cont<numerocon:
        #establish connection with client
        data,adrr=serverSocket.recvfrom(buffersize)
        print("Recibi conexion",cont)
        #Crea el thread para manejar la conexion
        thread=Thread(target= start_thread, args=(serverSocket,adrr))
        #Se agregan a la lista de conecciones las que van llegando
        connections.append(thread)
        cont+=1
    #Se recorre la lista de threads y se les da start con la tarea que tienen que hacer   
    for i in connections:
        i.start()


def start_thread(s,adrr):
    hashSha=hashlib.sha256()
    num_paquetes=0
    with open(file,'rb') as f:
        while True:
            data=f.read(buffersize)
            if not data:
                print ("termine de leer")
                #en este punto es necesario enviar el hash al cliente
                h=str(hashSha.hexdigest())
                print("Hash a enviar: "+h)
                #Se le envía con el encabezado HASH para poder encontrarlo después
                s.sendto(("HASH"+h).encode(),adrr)
                print("El numero de paquetes eviados es de ",num_paquetes)
                break
            hashSha.update(data)
            s.sendto(data,adrr)
            num_paquetes+=1
        
main()
