import socket


def check_port(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)


    result = sock.connect_ex((host, port))
    if result == 0:
        print(f"A por {port}, está aberta no host: {host}")
    else:
        print("Port {} is closed".format(port))

    sock.close()


host = '127.0.0.1'
port = 12345

check_port(host, port)
