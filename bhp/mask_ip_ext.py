import requests

def get_external_ip():
    # URL para obter o IP externo
    url = "https://api.ipify.org?format=json"

    # URL do proxy (substitua pelo proxy que você deseja usar)
    proxy = {
        'http': 'http://your_proxy_ip:your_proxy_port',
        'https': 'http://your_proxy_ip:your_proxy_port'
    }

    try:
        # Fazendo a solicitação através do proxy
        response = requests.get(url, proxies=proxy)
        response.raise_for_status()
        ip_info = response.json()
        return ip_info['ip']
    except requests.exceptions.RequestException as e:
        print(f"Erro ao obter o IP externo: {e}")
        return None

if __name__ == "__main__":
    ip = get_external_ip()
    if ip:
        print(f"Seu IP externo é: {ip}")
    else:
        print("Não foi possível obter o IP externo.")