import socket
"""
target_host = "www.google.com.br"
target_port = 80

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((target_host, target_port))
client.send("GET / HTTP/1.1\r\nHost: www.google.com.br\r\n\r\n")
response = client.recv(4096)
print(response.decode())"""


target_host = "0.0.0.0"
target_port = 9999

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((target_host, target_port))
client.send(b"GET / HTTP/1.1\r\nHost: www.google.com.br\r\n\r\n")
response = client.recv(4096)
print(response.decode())  # Decodificando a resposta de bytes para string

client.close()

