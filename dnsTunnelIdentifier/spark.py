from pyspark import SparkContext, SparkConf

spark_context = None

def initSpark(appName: str = 'test', master: str = 'local[*]') -> None:
  global spark_context
  conf = SparkConf().setAppName(appName).setMaster(master)
  conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
  conf.set("spark.sql.execution.arrow.enabled", "true")
  spark_context = SparkContext(conf=conf)
  spark_context.setLogLevel("ERROR")

def getSC() -> SparkContext:
  global spark_context
  return spark_context