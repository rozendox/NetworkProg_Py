"""
                                   formato:

mock/request mod
    | |
    | |
     |
   \\ //
    \ /
----------                                  ---------------
|        |  ----- http request --------->   |     app2/   |
|  app1  |  <----- http response --------   |     api/    |
|        |                                  |serv.extern  |
----------                                  ---------------



rode pytest testes_http.py
(rodamos testes 
"""

from typing import Literal, TypeAlias, get_args
import httpx
import respx

url_cotacao = "https://economia.awesomeapi.com.br/json/last/{}"

Moeda: TypeAlias = Literal['EUR', 'USD', 'BTC']


def cotacao(moeda: Moeda):
    code = f'{moeda}-BRL'
    try:
        response = httpx.get(
            url_cotacao.format(code), timeout=10
        )
        data = response.json()[code.replace('-', '')]
        return f'ultima cotacao: {data["high"]}'
    except KeyError:
        return f'Codigo de moeda invalido. Use {get_args(Moeda)}'
    except httpx.InvalidURL:
        return f'Codigo de moeda invalido. Use {get_args(Moeda)}'
    except httpx.ConnectError:
        return 'Erro de conexao. Tente novamente mais tarde.'
    except httpx.TimeoutException:
        return 'Erro de conexao. Tente novamente mais tarde.'


@respx.mock
def test_dolar():
    mocked_response = httpx.Response(
        200, json={'USDBRL': {'high': 5.7939}}
    )
    respx.get(
        url_cotacao.format('USD-BRL'),
    ).mock(mocked_response)
    result = cotacao('USD')
    assert result == "ultima cotacao: 5.7939"


@respx.mock
def test_moeda_errada():
    mocked_response = httpx.Response(200, json={})
    respx.get(
        url_cotacao.format('MDT-BRL'),
    ).mock(mocked_response)
    result = cotacao('MDT')  # moeda inexiste

    assert (
            result == "Codigo de moeda invalido. Use ('EUR', 'USD', 'BTC')"
    )


def test_moeda_erro_na_url():
    result = cotacao('\x11')
    assert (
            result == "Codigo de moeda invalido. Use ('EUR', 'USD', 'BTC')"
    )


@respx.mock
def test_erro_conexao():
    # ar
    respx.get(
        url_cotacao.format('USD-BRL')
    ).mock(side_effect=httpx.ConnectError)

    # act
    result = cotacao('USD')

    # ass (lol)
    assert result == 'Erro de conexao. Tente novamente mais tarde.'


@respx.mock
def test_erro_timeout():
    # ar
    respx.get(
        url_cotacao.format('USD-BRL')
    ).mock(side_effect=httpx.TimeoutException)

    # act
    result = cotacao('USD')

    # ass (lol)
    assert result == 'Erro de conexao. Tente novamente mais tarde.'

# print(cotacao('USD'))
# print(cotacao('EUR'))
