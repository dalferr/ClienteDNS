# ClienteDNS

Cliente DNS simple que obtiene la dirección IP asociada al nombre DNS de una máquina cualquiera.

## Configuración
Al inicio del script debemos indicar la dirección de nuestro servidor DNS (esta se encuentra en el fichero /etc/resolv.conf)
```python
# Mirar servidor DNS en fichero "/etc/resolv.conf"
DNS_DIR = "127.0.0.53"
DNS_PORT = 53
```

## Uso
```bash
Uso: python3 dns_cli.py <Nombre DNS de máquina>
```
### Ejemplo
Introducimos:
```bash
python3 dns_cli.py ehu.eus
```
Y nos devuelve:
```bash
Pregunta DNS a enviar:
 b'\x00\x01\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03ehu\x03eus\x00\x00\x01\x00\x01'
Respuesta recibida:
 b'\x00\x01\x81\x80\x00\x01\x00\x01\x00\x00\x00\x00\x03ehu\x03eus\x00\x00\x01\x00\x01\xc0\x0c\x00\x01\x00\x01\x00\x00\x01\xb6\x00\x04\x9e\xe3\x00A'
QR: 1
RCODE: 0000
ANCOUNT: 1
Apartado de Respuesta: b'\xc0\x0c\x00\x01\x00\x01\x00\x00\x01\xb6\x00\x04\x9e\xe3\x00A'
Bits de Offset: 11
Se emplea Offset.
Tipo de la Respuesta: 1
Tipo de la Clase: 1
TTL de respuesta: 438
RDLENGTH de respuesta: 4
RDATA (IP): 158.227.0.65
```
