from scapy.all import *

# Realiza traceroute para o host especificado
result, _ = traceroute("8.8.8.8", maxttl=20)

# Exibe o resultado
result.show()
