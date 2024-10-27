import threading
import paramiko
import subprocess
import warnings
warnings.filterwarnings(action='ignore', category=DeprecationWarning)

def ssh_command(ip, user, passwd, command):

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username =user, password = passwd)
    ssh_session = client.get_transport().open_session()
    if ssh_session.active():
        ssh_session.exec_command(command)
        print(ssh_session.recv(1024))
    return



if __name__ == '__main__':
    warnings.filterwarnings(action='ignore', category=DeprecationWarning)
    ssh_command('170.80.62.208', 'roxyp', 'lovespython', 'id')