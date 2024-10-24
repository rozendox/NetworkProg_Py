from scapy.all import *


# Função que será chamada para cada pacote capturado
def packet_callback(packet):
    print(packet.show())


# Inicia o sniffing na interface de rede padrão
sniff(prn=packet_callback, count=10)
