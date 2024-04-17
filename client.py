import socket
# le pido el telefono al cliente
telefono = input("Indique el numero de telefono: ")
#envio el telefono
parameters = f"telefono={telefono}"

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.220.41', 12345))
client_socket.sendall(parameters.encode())

response = client_socket.recv(1024)
print("Received:", response.decode())

client_socket.close()
