import requests


def get_location_by_ip(ip):
    url = f"https://ipinfo.io/{ip}/json"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        location = data.get("loc", "").split(",")
        if len(location) == 2:
            return {
                "latitude": location[0],
                "longitude": location[1],
                "city": data.get("city", "Unknown"),
                "region": data.get("region", "Unknown"),
                "country": data.get("country", "Unknown")
            }
        else:
            return "Localização não encontrada."
    else:
        return f"Erro ao obter localização: {response.status_code}"


if __name__ == "__main__":
    ip = input("Digite o IP: ")
    location = get_location_by_ip(ip)
    print(f"Localização do IP {ip}: {location}")
