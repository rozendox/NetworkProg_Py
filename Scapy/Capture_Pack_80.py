from scapy.all import *

# Função para exibir pacotes HTTP
def http_packet(packet):
    if packet.haslayer(Raw):
        print(packet[Raw].load)

# Captura pacotes na porta 80 (HTTP)
sniff(filter="tcp port 80", prn=http_packet, count=10)
