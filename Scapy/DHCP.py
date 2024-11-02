from scapy.config import conf
from scapy.arch import get_if_hwaddr
from scapy.layers.inet import IP, UDP
from scapy.layers.dhcp import BOOTP, DHCP
from scapy.layers.l2 import Ether
from scapy.sendrecv import sendp, AsyncSniffer
from scapy.volatile import RandInt
from time import sleep

meu_mac = get_if_hwaddr(conf.iface)

def dhcp_discover():
    pacote = Ether(src=meu_mac) / IP(src='0.0.0.0', dst='255.255.255.255') / UDP(sport=68, dport=67) / DHCP(options=[('message-type', 'discover'), 'end'])
    sendp(pacote, iface=conf.iface)

def dhcp_request(requested, server_ip):
    pacote = Ether(src=meu_mac) / IP(src='0.0.0.0', dst=server_ip) / UDP(sport=68, dport=67) / BOOTP(chaddr=meu_mac, xid=RandInt()) / DHCP(options=[('message-type', 'request'), ('server_id', server_ip), ('requested_addr', requested), 'end'])
    sendp(pacote, iface=conf.iface)

# Captura a resposta DHCP Offer
s = AsyncSniffer(filter='udp and port 67')  # Use port 67 para captar ofertas
s.start()
sleep(1)  # Aumenta o tempo para garantir a captura
dhcp_discover()
sleep(5)  # Aguarde a resposta do servidor
s.stop()

# Verifica se algo foi capturado
if len(s.results) < 2:
    print("Nenhum pacote DHCP recebido. Verifique a conexão com o servidor DHCP.")
else:
    offer = s.results[1]
    ip_server = offer[1].src
    ip_oferecido = offer.yiaddr

    # Captura o DHCP Request
    s = AsyncSniffer(filter='udp and port 67')  # Use port 67 novamente
    s.start()
    sleep(1)  # Aumenta o tempo para garantir a captura
    dhcp_request(ip_oferecido, ip_server)
    sleep(2)
    s.stop()

    # Verifique novamente se pacotes foram recebidos
    if len(s.results) == 0:
        print("Nenhum pacote DHCP Request recebido.")
    else:
        s.results.summary()
