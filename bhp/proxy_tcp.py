import sys
import socket
import threading

from cv2 import data


def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    # cria a a conexão, o af diz que vai ser IPV4, e o sock stream diz que será um client tcp
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((local_host, local_port))
    except:
        print("[!!] Failed to listen on % S:% d", (local_host, local_port))
        print("[!!] Check for other listening sockets or correct ¬ ;permissions.")
        sys.exit(0)

    print("[!!] Failed  %s:%d" % (local_host, local_port))
    server.listen(5)

    while True:
        client_socket, addr = server.accept()

        # print out the local conection info.
        print("[===>] Received incoming connection from  %s:%d" % addr[0], addr[1])
        # start a thread --
        proxy_thread = threading.Thread(target=
                                        proxy_handler,
                                        args=(client_socket, remote_host, remote_port, receive_first))

        proxy_thread.start()


def main():
    # no fancy command-line parsing here
    if len(sys.argv[1:]) != 3:
        print("usage: ./proxy_tcp.py [localhost] [localport] [remotehost] [remoteport] [receive_first]")
        print("example: ./proxy_tcp.py 127.0.0.1 9000 10.12.132.1 9000 True")
        sys.exit(0)

    # setup local liste. par.

    local_host = sys.argv[1]
    local_port = int(sys.argv[2])

    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])

    receive_first = sys.argv[5]
    if "True" in receive_first:
        receive_first = True
    else:
        receive_first = False

    server_loop(local_host, local_port, remote_host, remote_port, receive_first)

def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))
    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)
        if len(remote_buffer):
            print("[<==] Sending %d bytes to localhost. " % len(remote_buffer))
            client_socket(remote_buffer)


    # read from local
    while True:
        local_buffer = receive_from(client_socket)

        if len(local_buffer):
            print("[==>] Received %d bytes from localhost. " % len(local_buffer))
            hexdump(local_buffer)

            local_buffer = request_handler(local_buffer)
            remote_socket.send(local_buffer)
            print("[==>] Sent to remote.")

    # receive back the response

    remote_buffer = receive_from(remote_socket)

    if len(remote_buffer):
        print("[<==] Received %d bytes from remote. " % len(remote_buffer))
        hexdump(remote_buffer)

        remote_buffer = request_handler(remote_buffer)
        client_socket.send(remote_buffer)
        print("[<==] Sent to remote.")

    if not len(local_buffer) or not len(remote_buffer):
        client_socket.close()
        remote_socket.close()
        print("[*] No more Data, Closing connection.")

# http://code.activestate.com/recipes/142812-hex-dumper/
def hexdump(src, length=16):
    result = []
    digits = 4 if isinstance(src, bytes) else 2
    for i in range(0, len(src), length):
        s = src[i:i+length]
        hexa = b' '.join(["%0*X" % (digits, ord(x)) for x in s])
        text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.' for x in s])
        result.append( b"%04X   %-*s   %s" % (i, length*(digits + 1), hexa,text))
    print(b'\n'.join(result))


def receive_from(connection):
    buffer = ""
    connection.settimeout(2)

    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break
    except: # fixme -> improve this error handling
        pass
    return buffer

def request_handler(buffer):
    return buffer

def response_handler(buffer):
    return buffer


if __name__ == "__main__":
    main()
