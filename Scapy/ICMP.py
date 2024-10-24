from scapy.all import *


# Envia um pacote ICMP (ping) para o host especificado
pkt = IP(dst="8.8.8.8") / ICMP()
response = sr1(pkt, timeout=1)

# Verifica se houve resposta
if response:
    response.show()
else:
    print("Sem resposta")
