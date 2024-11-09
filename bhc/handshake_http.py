import socket

def http_handshake(host, port = 80):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print(f"Connection established: {host}:{port}")

        request = f"GET/ HTTP/1.1\r\nHost:{host}\r\nConnection: close\r\n\r\n"
        s.sendall(request.encode())

        response = s.recv(4096)
        print("reposta do servidor:", response.decode())

http_handshake("www.google.com")