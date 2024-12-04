import datetime

from config import functions
from config import vars
from scripts import extract

def etl(modo: str) -> None:
    dia_util_anterior = functions.busca_ultimo_dia_util(datetime.date.today())
    ultimo_ano_com_dia_util = dia_util_anterior.year
    ano_inicial = ultimo_ano_com_dia_util if modo == 'incremental' else vars.ano_inicial
    anos_a_serem_processados = range(ano_inicial, ultimo_ano_com_dia_util + 1)
    for ano in anos_a_serem_processados:
        extract.baixa_historico_precos(ano)