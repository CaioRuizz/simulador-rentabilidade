import datetime
import pyspark.sql.dataframe
import pyspark.sql.functions as sf

def filtra_e_seleciona_historico_precos(precos_historicos: pyspark.sql.dataframe.DataFrame, data_inicial: datetime.date) -> pyspark.sql.dataframe.DataFrame:
    return precos_historicos.filter(
        (sf.col('Data') >= data_inicial) &
        (sf.col('CodBdi').isin([2, 12]) | sf.col('Especificacao').isin('BDR', 'CI'))
    ).select(
        'Data',
        'CodNeg',
        'PrecoUltimo',
    )