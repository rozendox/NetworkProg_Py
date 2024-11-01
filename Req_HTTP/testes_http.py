from typing import Literal, TypeAlias
import httpx

url_cotacao = "https://economia.awesomeapi.com.br/json/last/{}"

Moeda: TypeAlias = Literal['EUR', 'USD']


def cotacao(moeda: Moeda):
    code = f'{moeda}-BRL'
    response = httpx.get(url_cotacao.format(code))
    data = response.json()[code.replace('-', '')]

    return f'ultima cotacao: {data["high"]}'

def test_dolar():
    result = cotacao('USD')
    assert result == "ultima cotacao: 5.7939"


print(cotacao('USD'))
print(cotacao('EUR'))
