import datetime
import functools

import requests


def verifica_fim_de_semana(date: datetime.date) -> bool:
    # Verifica se o dia é sábado (5) ou domingo (6)
    return date.weekday() >= 5


def verifica_ano_novo(date: datetime.date) -> bool:
    # Verifica se a data é 1º de janeiro
    return date.month == 1 and date.day == 1


def busca_ultimo_dia_util(date: datetime.date) -> datetime.date:
    # Decrementa o dia por 1 (um dia anterior)
    date -= datetime.timedelta(days=1)

    # Verifica se é feriado ou primeiro de Janeiro
    while verifica_fim_de_semana(date) or verifica_ano_novo(date):
        
        # Decrementa o dia por 1 (um dia anterior)
        date -= datetime.timedelta(days=1)
        
    return date


@functools.cache
def navegador_get(url: str) -> requests.Response:
    # Definindo os headers para imitar o Firefox
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # Fazendo a requisição HTTP com os headers
    return requests.get(url, headers=headers)