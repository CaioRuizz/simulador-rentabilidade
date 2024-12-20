import zipfile
import io
import os
import re
import typing
import pathlib

import requests
import pandas as pd
import pyspark.sql.dataframe
import pyspark.sql.functions as sf

from config import vars
from config import functions

spark = vars.spark

def _encontra_arquivo_mais_recente(diretorio: str) -> typing.Union[str, None]:
    arquivos = [f for f in os.listdir(diretorio) if os.path.isfile(os.path.join(diretorio, f))]

    if not arquivos:
        print("O diretório está vazio")
        return None

    datas_modificacao = [os.path.getmtime(os.path.join(diretorio, f)) for f in arquivos]

    indice_mais_recente = datas_modificacao.index(max(datas_modificacao))

    arquivo_mais_recente = arquivos[indice_mais_recente]

    return os.path.join(diretorio, arquivo_mais_recente)


def baixa_historico_precos(ano: int) -> None:
    pasta_downloads = os.path.join(vars.base_path, 'downloads')

    diretorio = pathlib.Path(pasta_downloads)

    diretorio.mkdir(parents=True, exist_ok=True)

    print(f'Baixando dados do ano {ano}')

    zip_file_url = f'https://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_A{ano}.ZIP'

    r = requests.get(zip_file_url, verify=False)

    print(f'Extraindo arquivo do ano {ano}')

    z = zipfile.ZipFile(io.BytesIO(r.content))

    z.extractall(pasta_downloads)

    print(f'Formatando arquivo do ano {ano}')

    arquivo_cru = _encontra_arquivo_mais_recente(pasta_downloads)

    if arquivo_cru is None:
        raise FileNotFoundError(f'Nenhum arquivo foi encontrado no ano {ano}')

    df = spark.read.text(arquivo_cru)

    df = df.select(
        df.value.substr(3, 8).alias("Data"),
        df.value.substr(11, 2).alias("CodBdi"),
        df.value.substr(13, 12).alias("CodNeg"),
        df.value.substr(25, 3).alias("TipoMercado"),
        df.value.substr(28, 12).alias("Empresa"),
        df.value.substr(40, 10).alias("Especificacao"),
        df.value.substr(50, 3).alias("Prazo"),
        df.value.substr(53, 4).alias("Moeda"),
        df.value.substr(57, 13).alias("PrecoAbertura"),
        df.value.substr(70, 13).alias("PrecoMaximo"),
        df.value.substr(83, 13).alias("PrecoMinimo"),
        df.value.substr(96, 13).alias("PrecoMedio"),
        df.value.substr(109, 13).alias("PrecoUltimo"),
        df.value.substr(122, 13).alias("MelhorOfertaCompra"),
        df.value.substr(135, 13).alias("MelhorOfertaVenda"),
        df.value.substr(148, 5).alias("NumeroNegocio"),
        df.value.substr(153, 18).alias("QuantidadeNegociada"),
        df.value.substr(171, 18).alias("VolumeFinanceiro"),
        df.value.substr(189, 12).alias("PrecoExercicio"),
        df.value.substr(202, 1).alias("IndicadorCorrecao"),
        df.value.substr(203, 8).alias("DataVencimento"),
        df.value.substr(211, 7).alias("FatorCotacao"),
        df.value.substr(218, 13).alias("PrecoExercicioPontos"),
        df.value.substr(231, 12).alias("CodIsin"),
        df.value.substr(243, 3).alias("NumeroDistribuicao"),
    ).where(sf.trim(sf.col("QuantidadeNegociada")) != '')
    
    df = df.withColumn("Data", sf.to_date(sf.substring(sf.trim(sf.col("Data")), 1, 8), "yyyyMMdd"))
    df = df.withColumn("CodBdi", sf.trim(sf.col("CodBdi").cast("integer")))
    df = df.withColumn("CodNeg", sf.trim(sf.col("CodNeg")))
    df = df.withColumn("TipoMercado", sf.trim(sf.col("TipoMercado").cast("integer")))
    df = df.withColumn("Empresa", sf.trim(sf.col("Empresa")))
    df = df.withColumn("Especificacao", sf.split(sf.col("Especificacao"), " ")[0])
    df = df.withColumn("Prazo", sf.trim(sf.col("Prazo")).cast("integer"))
    df = df.withColumn("Moeda", sf.trim(sf.col("Moeda")))
    df = df.withColumn("PrecoAbertura", sf.trim(sf.col("PrecoAbertura")).cast("Decimal(18, 2)") / 100)
    df = df.withColumn("PrecoMaximo", sf.trim(sf.col("PrecoMaximo")).cast("Decimal(18, 2)") / 100)
    df = df.withColumn("PrecoMinimo", sf.trim(sf.col("PrecoMinimo")).cast("Decimal(18, 2)") / 100)
    df = df.withColumn("PrecoMedio", sf.trim(sf.col("PrecoMedio")).cast("Decimal(18, 2)") / 100)
    df = df.withColumn("PrecoUltimo", sf.trim(sf.col("PrecoUltimo")).cast("Decimal(18, 2)") / 100)
    df = df.withColumn("MelhorOfertaCompra", sf.trim(sf.col("MelhorOfertaCompra")).cast("Decimal(18, 2)") / 100)
    df = df.withColumn("MelhorOfertaVenda", sf.trim(sf.col("MelhorOfertaVenda")).cast("Decimal(18, 2)") / 100)
    df = df.withColumn("NumeroNegocio", sf.trim(sf.col("NumeroNegocio")).cast("Decimal(18, 2)"))
    df = df.withColumn("QuantidadeNegociada", sf.trim(sf.col("QuantidadeNegociada")).cast("Decimal(18, 2)"))
    df = df.withColumn("VolumeFinanceiro", sf.trim(sf.col("VolumeFinanceiro")).cast("Decimal(18, 2)"))
    df = df.withColumn("PrecoExercicio", sf.trim(sf.col("PrecoExercicio")).cast("Decimal(18, 2)"))
    df = df.withColumn("IndicadorCorrecao", sf.trim(sf.col("IndicadorCorrecao")).cast("integer"))
    df = df.withColumn("DataVencimento", sf.to_date(sf.substring(sf.trim(sf.col("DataVencimento")), 1, 8), "yyyyMMdd"))
    df = df.withColumn("FatorCotacao", sf.trim(sf.col("FatorCotacao")).cast("bigint"))
    df = df.withColumn("PrecoExercicioPontos", sf.trim(sf.col("PrecoExercicioPontos")).cast("bigint"))
    df = df.withColumn("CodIsin", sf.trim(sf.col("CodIsin")))
    df = df.withColumn("NumeroDistribuicao", sf.trim(sf.col("NumeroDistribuicao")).cast("bigint"))


    print(f'Ano {ano}: {df.count()} registros')

    write_dir = os.path.join(vars.base_path, 'spark_files', 'bronze', 'negociacao', f'Ano={ano}')

    print(f'Gravando arquivo formatado do ano {ano} no diretório {write_dir}')

    df.write.mode('overwrite').parquet(write_dir)

    print(f'Excluindo arquivo cru do ano {ano}')

    os.remove(arquivo_cru)


def _buscar_id_ativo(ticker: str) -> int:
    response = functions.navegador_get(f"https://investidor10.com.br/acoes/{ticker}/")

    line = [*filter(lambda x: 'dispatch' in x, response.text.split('\n'))][0]

    return int(re.findall(r'[0-9]+', line)[0])


def baixa_quantidade_acoes(ticker: str) -> int:
    response = functions.navegador_get(f"https://investidor10.com.br/acoes/{ticker}/")
    linhas = response.text.split('\n')
    line = [*filter(lambda x: 'Nº total de papeis' in x, linhas)][0]
    indice = response.text.split('\n').index(line)
    html = ''.join(linhas[indice:indice + 7])
    matches = re.findall(r'[0-9\.]+', html)
    return int(max(matches, key=len).replace('.', ''))


def baixa_resultados_trimestrais(ticker: str) -> pyspark.sql.dataframe.DataFrame:
    stock_id = _buscar_id_ativo(ticker)
    
    response = functions.navegador_get(f'https://investidor10.com.br/api/balancos/balancoresultados/chart/{stock_id}/15/quarterly/')
    
    data = response.json()
    
    # Suponha que os dados estão carregados na variável 'dados'
    # Extraindo o cabeçalho e os valores das linhas
    colunas = data[0]
    valores = data[1:]

    df = pd.DataFrame(valores, columns=colunas)
    
    df['index'] = df['#']
    
    del df['#']

    return spark.createDataFrame(df)


def baixa_historico_dividendos(ticker: str) -> pyspark.sql.dataframe.DataFrame:
    response = functions.navegador_get(f"https://investidor10.com.br/acoes/{ticker}/")
    data = response.text
    df = pd.read_html(io.StringIO(data))[0] # type: ignore
    df.Valor = df['Valor'] / 100000000
    df['Imposto'] = (df['Tipo'] != 'Dividendos') * 0.15 * df['Valor']
    df['ValorLiquido'] = df['Valor'] - df['Imposto']
    return spark.createDataFrame(df)