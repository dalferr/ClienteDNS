#!/usr/bin/env python3

import socket, sys

# Mirar servidor DNS en fichero "/etc/resolv.conf"
DNS_DIR = "127.0.0.53"
DNS_PORT = 53

if len( sys.argv ) != 2:
	print( "Uso: python3 {} <Nombre DNS de máquina>".format( sys.argv[0] ) )
	exit( 1 )

nombre_dns = sys.argv[1]

serv_dns = (DNS_DIR, DNS_PORT)

s = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )

# HeaderSection

ID = (1).to_bytes(2, 'big')
FLAGS = (1).to_bytes(2, 'little')
QDCOUNT = (1).to_bytes(2, 'big')
ANCOUNT = (0).to_bytes(2, 'big')
NSCOUNT = (0).to_bytes(2, 'big')
ARCOUNT = (0).to_bytes(2, 'big')

HEADER = ID + FLAGS + QDCOUNT + ANCOUNT + NSCOUNT + ARCOUNT

# Question section
QNAME = b''

sep = nombre_dns.split(".")
for i in sep:
    QNAME = QNAME + len(i).to_bytes(1, 'big') + i.encode()
    
QNAME = QNAME + b'\x00'

QTYPE = (1).to_bytes(2, 'big')
QCLASS = (1).to_bytes(2, 'big')

QUESTION = QNAME + QTYPE + QCLASS

#--

buf = HEADER + QUESTION
longitud_preg = len(buf)

# -- Pregunta DNS completa --

print( "Pregunta DNS a enviar:\r\n", buf )
# Enviar pregunta DNS
s.sendto( buf, serv_dns )
# Recibir respuesta
buf = s.recv( 1024 )
print( "Respuesta recibida:\r\n", buf )

#######ANALISIS RESPUESTA

ID2 = buf[0:2]

if(ID != ID2):
    print("El ID no coincide. La respuesta no es válida.")
    exit(1)
else:

    byte_24 = bin(int.from_bytes(buf[2:4], 'big'))[2:]
    QR2 = byte_24[0]
    RCODE2 = byte_24[12:]
    
    print("QR: " + QR2)
    print("RCODE: " + RCODE2)
    
    if(QR2 != '1' or RCODE2 != '0000'):
            print("El QR o RCODE muestran un error. Respuesta inválida.")
            exit(1)
    
    ANCOUNT2 = int.from_bytes(buf[6:8], 'big')
    print("ANCOUNT: " + str(ANCOUNT2))
    if(ANCOUNT2 != 1):
        print("El ANCOUNT es distinto de 1. Respuesta inválida.")
        exit(1)
    
    ANSWER2 = buf[longitud_preg:]
    print("Apartado de Respuesta: " + str(ANSWER2))
    
    byte0 = bin(int.from_bytes(ANSWER2[0:1],'big'))[2:4]
    print("Bits de Offset: " + byte0)
    if(byte0 == '11'):
        print("Se emplea Offset.")
        TYPE2 = int.from_bytes(ANSWER2[2:4],'big')
        print("Tipo de la Respuesta: " + str(TYPE2))
        CLASS2 = int.from_bytes(ANSWER2[4:6],'big')
        print("Tipo de la Clase: " + str(CLASS2))
        TTL2 = int.from_bytes(ANSWER2[6:10],'big')
        print("TTL de respuesta: " + str(TTL2))
        RDL2 = int.from_bytes(ANSWER2[10:12],'big')
        print("RDLENGTH de respuesta: " + str(RDL2))
        RDATA2 = socket.inet_ntoa(ANSWER2[12:])
        print("RDATA (IP): " + RDATA2)


s.close()

