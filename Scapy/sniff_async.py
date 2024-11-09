from scapy.sendrecv import AsyncSniffer
from scapy.all import get_if_list
from time import sleep

print("interfaces de rede disp")
print(get_if_list())

interface = 'Ethernet'

s = AsyncSniffer(
    filter='udp and port 68', iface='interface'
)
s.start()

sleep(5)

# s.stop()
print(s.results)