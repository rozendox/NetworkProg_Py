from scapy.all import *
import time

def scan_ports(ip, ports):
    results = {}
    for port in ports:
        packet = IP(dst=ip) / TCP(dport=port, flags="S")
        print(f"Escaneando porta {port}...")
        response = sr1(packet, timeout=1, verbose=0)
        if response is None:
            results[port] = "Fechado"
        else:
            results[port] = "Aberto"
        print(f"Porta {port}: {results[port]}")
    return results

if __name__ == "__main__":
    ip = input("Digite o IP: ")
    ports = range(1, 1024)  # Escaneando portas de 1 a 1023
    results = scan_ports(ip, ports)
    print("\nResultados do escaneamento:")
    for port, status in results.items():
        print(f"Porta {port}: {status}")
