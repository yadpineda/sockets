import socket
import mysql.connector

# conexion al socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0',12345))
server_socket.listen()

# base de datos mysql configuracion
db_config = {
	'host': 'localhost',
	'user': 'root',
	'password': '',
	'database': 'clientes'
}
# funcion para ejecutar consultas
def execute_query(query):
	connectionsql = None
	try:
		connectionsql = mysql.connector.connect(**db_config)
		cursor = connectionsql.cursor()
		cursor.execute(query)
		results = cursor.fetchall()
		connectionsql.commit()
		return results

	except mysql.connector.Error as error:
		print("Error executing query:",error)

	finally:
		if connectionsql is not None and connectionsql.is_connected():
			cursor.close()
			connectionsql.close()

print("Socket server is listening for connections...")

while True: # configuro los sockets esperando las conexiones desde el cliente
	client_socket, client_address = server_socket.accept()
	print(f"Accepted connection from {client_address}")
	data = client_socket.recv(1024)
	received_data = data.decode()
	params = received_data.split('&')
	# recibo el numero de telefono desde el cliente
	telefono = None
	for param in params:
		key, value = param.split('=')
		if key == 'telefono':
			telefono = value
			break
	# si existe un numero de telefono realizo la consulta a la base de datos y le muestro los datos al cliente
	if telefono is not None:
		resultsQuery = execute_query(f"SELECT personas.*, ciud_nombre FROM personas LEFT JOIN ciudades ON personas.dir_ciud_id = ciudades.ciud_id WHERE dir_tel = '{telefono}'")
		client_socket.sendall(b"Persona encontrada: ")
		client_socket.sendall(str(resultsQuery).encode())
	else:
		print('no indico telefono')
	client_socket.close()
