import os

from pyspark.sql import SparkSession

base_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')
ano_inicial = 2014

spark = SparkSession.Builder().getOrCreate()