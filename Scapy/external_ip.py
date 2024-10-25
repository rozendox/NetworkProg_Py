import requests

def get_external_ip():
    try:
        response = requests.get('https://httpbin.org/ip')
        response.raise_for_status()  # Isso garante que qualquer erro de rede seja levantado como uma exceção
        ip_info = response.json()
        return ip_info['origin']
    except requests.RequestException as e:
        print(f"Erro ao obter o IP externo: {e}")
        return None

if __name__ == "__main__":
    ip = get_external_ip()
    if ip:
        print(f"Seu IP externo é: {ip}")
    else:
        print("Não foi possível obter o IP externo.")