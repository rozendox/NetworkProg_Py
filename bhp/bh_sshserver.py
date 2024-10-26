import socket
import paramiko
import threading
import sys

host_key = paramiko.RSAKey(filename='test_rsa.key')


class Server(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED

    def check_auth_password(self, username, password):
        if username == 'roxyp' and password == '<lovepython>':
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED


if len(sys.argv) < 3:
    print("Usage: script.py <server_ip> <ssh_port>")
    sys.exit(1)

server = sys.argv[1]
ssh_port = int(sys.argv[2])

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((server, ssh_port))
    sock.listen(100)
    print('[+] LISTENING FOR CONNECTION ...')
    client, addr = sock.accept()
except Exception as e:
    print('Listen failed: ' + str(e))
    sys.exit(1)

print('[+] GOT A CONNECTION TO ' + addr[0] + ':' + str(addr[1]))

try:
    bhSession = paramiko.Transport(client)
    bhSession.add_server_key(host_key)
    server = Server()
    try:
        bhSession.start_server(server=server)
    except paramiko.SSHException:
        print('[-] SSH negotiation failed')

    chan = bhSession.accept(20)
    print('[+] AUTHENTICATION SUCCESSFUL!')

    if chan is None:
        print("[-] No channel.")
        bhSession.close()
        sys.exit(1)

    chan.send('WELCOME TO BH_SSH'.encode())

    while True:
        command = input("Enter command: ").strip()
        if command != 'exit':
            chan.send(command.encode())
            print(chan.recv(1024).decode() + '\n')
        else:
            chan.send('exit'.encode())
            print("EXITING...")
            bhSession.close()
            break

except Exception as e:
    print("[-] CAUGHT EXCEPTION: " + str(e))
    try:
        bhSession.close()
    except:
        pass
    sys.exit(1)


