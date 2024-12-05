import datetime
import os

from config import functions
from config import vars
from scripts import extract
from scripts import transform

spark = vars.spark

def etl(modo: str) -> None:
    dia_util_anterior = functions.busca_ultimo_dia_util(datetime.date.today())
    data_inicial = dia_util_anterior - datetime.timedelta(days=7) if modo == 'incremental' else datetime.date(vars.ano_inicial, 1, 1)
    ultimo_ano_com_dia_util = dia_util_anterior.year
    ano_inicial = ultimo_ano_com_dia_util if modo == 'incremental' else vars.ano_inicial
    anos_a_serem_processados = range(ano_inicial, ultimo_ano_com_dia_util + 1)
    for ano in anos_a_serem_processados:
        extract.baixa_historico_precos(ano)
    precos_historicos_bronze = spark.read.parquet(os.path.join(vars.base_path, 'spark_files', 'bronze', 'negociacao'))
    precos_historicos_silver = transform.filtra_e_seleciona_historico_precos(precos_historicos_bronze, data_inicial)
    print(f"{precos_historicos_silver.select('CodNeg').distinct().count() = }")
    print(f'{precos_historicos_silver.count() = }')