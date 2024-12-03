import datetime

from config import functions
from config import vars

def etl(modo: str) -> None:
    dia_util_anterior = functions.busca_ultimo_dia_util(datetime.date.today())
    ultimo_ano_com_dia_util = dia_util_anterior.year
    anos_a_serem_processados = range(ultimo_ano_com_dia_util if modo == 'incremental' else vars.ano_inicial, ultimo_ano_com_dia_util + 1)
    print(modo)
    print(dia_util_anterior)
    print(ultimo_ano_com_dia_util)
    print(anos_a_serem_processados)