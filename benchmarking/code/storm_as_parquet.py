# Databricks notebook source
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField, StringType, IntegerType
from pyspark.sql.types import ArrayType, DoubleType, BooleanType
from pyspark.sql.functions import *
from builtins import round as pyround

# COMMAND ----------

schema_details = StructType([
    StructField("BEGIN_YEARMONTH", StringType(),True),
    StructField("BEGIN_DAY", StringType(),True),
    StructField("BEGIN_TIME", StringType(),True),
    StructField("END_YEARMONTH", StringType(),True),
    StructField("END_DAY", StringType(),True),
    StructField("END_TIME", StringType(),True),
    StructField("EPISODE_ID", IntegerType(),True),
    StructField("EVENT_ID", IntegerType(),True),
    StructField("STATE", StringType(),True),
    StructField("STATE_FIPS", IntegerType(),True),
    StructField("YEAR", IntegerType(),True),
    StructField("MONTH_NAME", StringType(),True),
    StructField("EVENT_TYPE", StringType(),True),
    StructField("CZ_TYPE", StringType(),True),
    StructField("CZ_FIPS", IntegerType(),True),
    StructField("CZ_NAME", StringType(),True),
    StructField("WFO", StringType(),True),
    StructField("BEGIN_DATE_TIME", StringType(),True),
    StructField("CZ_TIMEZONE", StringType(),True),
    StructField("END_DATE_TIME", StringType(),True),
    StructField("INJURIES_DIRECT", IntegerType(),True),
    StructField("INJURIES_INDIRECT", IntegerType(),True),
    StructField("DEATHS_DIRECT", IntegerType(),True),
    StructField("DEATHS_INDIRECT", IntegerType(),True),
    StructField("DAMAGE_PROPERTY", StringType(),True),
    StructField("DAMAGE_CROPS", StringType(),True),
    StructField("SOURCE", StringType(),True),
    StructField("MAGNITUDE", DoubleType(),True),
    StructField("MAGNITUDE_TYPE", StringType(),True),
    StructField("FLOOD_CAUSE", StringType(),True),
    StructField("CATEGORY", IntegerType(),True),
    StructField("TOR_F_SCALE", StringType(),True),
    StructField("TOR_LENGTH", DoubleType(),True),
    StructField("TOR_WIDTH", IntegerType(),True),
    StructField("TOR_OTHER_WFO", StringType(),True),
    StructField("TOR_OTHER_CZ_STATE", StringType(),True),
    StructField("TOR_OTHER_CZ_FIPS", IntegerType(),True),
    StructField("TOR_OTHER_CZ_NAME", StringType(),True),
    StructField("BEGIN_RANGE", IntegerType(),True),
    StructField("BEGIN_AZIMUTH", StringType(),True),
    StructField("BEGIN_LOCATION", StringType(),True),
    StructField("END_RANGE", IntegerType(),True),
    StructField("END_AZIMUTH", StringType(),True),
    StructField("END_LOCATION", StringType(),True),
    StructField("BEGIN_LAT", DoubleType(),True),
    StructField("BEGIN_LON", DoubleType(),True),
    StructField("END_LAT", DoubleType(),True),
    StructField("END_LON", DoubleType(),True),
    StructField("EPISODE_NARRATIVE",StringType(),True),
    StructField("EVENT_NARRATIVE",StringType(),True),
    StructField("DATA_SOURCE", StringType(),True)
])

# COMMAND ----------

schema_fatalities = StructType([
    StructField("FAT_YEARMONTH", StringType(),True),
    StructField("FAT_DAY", StringType(),True),
    StructField("FAT_TIME", StringType(),True),
    StructField("FATALITY_ID", IntegerType(),True),
    StructField("EVENT_ID", IntegerType(),True),
    StructField("FATALITY_TYPE", StringType(),True),
    StructField("FATALITY_DATE", StringType(),True),
    StructField("FATALITY_AGE", IntegerType(),True),
    StructField("FATALITY_SEX", StringType(),True),
    StructField("FATALITY_LOCATION",IntegerType(),True),
    StructField("EVENT_YEARMONTH",StringType(),True)
])

# COMMAND ----------

storage_account_name = "pipelinestorageacctaus"
storage_account_access_key = "-"
spark_blob_container = "sparkstorestorm"
blob_container = "allfiles"
"""
for mount in dbutils.fs.mounts():
    print(mount.mountPoint == '/mnt/storm')

if not any(mount.mountPoint == '/mnt/storm/' for mount in dbutils.fs.mounts()):
    try:
        dbutils.fs.mount(
        source = "wasbs://{}@{}.blob.core.windows.net".format(spark_blob_container, storage_account_name),
        mount_point = "/mnt/storm",
        extra_configs = {'fs.azure.account.key.' + storage_account_name + '.blob.core.windows.net': storage_account_access_key})
    except Exception as e:
        print("already mounted. Try to unmount first")

display(dbutils.fs.ls("dbfs:/mnt/mountfolder/data"))
"""

# COMMAND ----------

detPath = "wasbs://allfiles@pipelinestorageacctaus.blob.core.windows.net/details/*.gz"

df_details = spark.read.format("csv").option("header", True).schema(schema_details).load("wasbs://allfiles@pipelinestorageacctaus.blob.core.windows.net/details/*.gz")

print('count of details loaded to spark: ' +  str(df_details.count()))

# COMMAND ----------

print('count of fatalities loaded to spark: ' + str(df_fatalities.count()))

# COMMAND ----------

print('count of fatalities loaded to spark partitioned as parquet: '+str(fatalities_autopart.count()))

# COMMAND ----------

df_fatalities.groupBy('FATALITY_TYPE').count().show()

# COMMAND ----------

fatalities_autopart.groupBy('FATALITY_TYPE').count().show()

# COMMAND ----------

print('counting full fatalities:')
print(f'\tdefault partition vs non-partitioned speedup = {pyround(.62/.3,2)}x')
print('\ncounting fatalities by fatality_type:')
print(f'\tdefault partition vs non-partitioned speedup = {pyround(.71/.37,2)}x')

# COMMAND ----------

fatPath = "wasbs://"  + blob_container + "@" + storage_account_name + ".blob.core.windows.net/fatalities/*.gz"

df_fatalities = spark.read.format("csv").option("header", True).schema(schema_fatalities).load(fatPath)

print('count of fatalities loaded to spark: ' + str(df_fatalities.count()))

# COMMAND ----------

df_details.createOrReplaceTempView("details")

# COMMAND ----------

def mon_to_num(string):
    m = {
        'jan':'01',
        'feb':'02',
        'mar':'03',
        'apr':'04',
        'may':'05',
        'jun':'06',
        'jul':'07',
        'aug':'08',
        'sep':'09',
        'oct':'10',
        'nov':'11',
        'dec':'12'}
    s = string.strip()[:3].lower()

    try:
        out = m[s]
        return out
    except:
        raise ValueError('Not a month')
spark.udf.register("mon_to_num", lambda str: mon_to_num(str) if not str is None else "" , StringType())


# COMMAND ----------

details_ltd =\
    spark.sql("SELECT \
        TO_TIMESTAMP(CONCAT(LEFT(BEGIN_M_DATE_TIME,3),mon_to_num(SUBSTR(BEGIN_M_DATE_TIME,4,3)),RIGHT(BEGIN_M_DATE_TIME,5),RIGHT(BEGIN_DATE_TIME,9)),'dd-MM-yyyy HH:mm:ss') AS BEGIN_TIMESTAMP,\
        TO_TIMESTAMP(CONCAT(LEFT(END_M_DATE_TIME,3),mon_to_num(SUBSTR(END_M_DATE_TIME,4,3)),RIGHT(END_M_DATE_TIME,5),RIGHT(END_DATE_TIME,9)),'dd-MM-yyyy HH:mm:ss') AS END_TIMESTAMP,\
        EPISODE_ID,EVENT_ID,STATE,CZ_NAME AS LOCALITY,EVENT_TYPE,\
        (DEATHS_DIRECT+DEATHS_INDIRECT) AS DEATHS,\
        (INJURIES_DIRECT+INJURIES_INDIRECT) AS INJURIES,\
            CASE\
            WHEN RIGHT(DAMAGE_PROPERTY, 1) = 'K' THEN ROUND(1000.00*CAST(LEFT(DAMAGE_PROPERTY,LENGTH(DAMAGE_PROPERTY)-1) AS DECIMAL(5,2)),2)\
            WHEN RIGHT(DAMAGE_PROPERTY, 1) = 'M' THEN ROUND(1000000.00*CAST(LEFT(DAMAGE_PROPERTY,LENGTH(DAMAGE_PROPERTY)-1) AS DECIMAL(5,2)),2)\
            WHEN RIGHT(DAMAGE_PROPERTY, 1) = 'B' THEN ROUND(1000000000.00*CAST(LEFT(DAMAGE_PROPERTY,LENGTH(DAMAGE_PROPERTY)-1) AS DECIMAL(5,2)),2)\
            WHEN DAMAGE_PROPERTY IS NULL THEN 0.00\
            ELSE ROUND(CAST(DAMAGE_PROPERTY AS DECIMAL(5,2)),2)\
        END AS DAMAGED_PROPERTY,\
            CASE\
            WHEN RIGHT(DAMAGE_CROPS, 1) = 'K' THEN ROUND(1000.00*CAST(LEFT(DAMAGE_CROPS,LENGTH(DAMAGE_CROPS)-1) AS DECIMAL(5,2)),2)\
            WHEN RIGHT(DAMAGE_CROPS, 1) = 'M' THEN ROUND(1000000.00*CAST(LEFT(DAMAGE_CROPS,LENGTH(DAMAGE_CROPS)-1) AS DECIMAL(5,2)),2)\
            WHEN RIGHT(DAMAGE_CROPS, 1) = 'B' THEN ROUND(1000000000.00*CAST(LEFT(DAMAGE_CROPS,LENGTH(DAMAGE_CROPS)-1) AS DECIMAL(5,2)),2)\
            WHEN DAMAGE_CROPS IS NULL THEN 0.00\
            ELSE ROUND(CAST(DAMAGE_CROPS AS DECIMAL(5,2)),2)\
        END AS DAMAGED_CROPS,\
        BEGIN_LAT,BEGIN_LON,END_LAT,END_LON\
        FROM (SELECT \
            CASE WHEN CAST(SUBSTR(BEGIN_DATE_TIME,8,2) AS INTEGER) > 30 THEN LEFT(CONCAT(LEFT(BEGIN_DATE_TIME,7),'19',RIGHT(BEGIN_DATE_TIME,11)),11)\
            ELSE LEFT(CONCAT(LEFT(BEGIN_DATE_TIME,7),'20',RIGHT(BEGIN_DATE_TIME,11)),11)\
        END AS BEGIN_M_DATE_TIME,\
            CASE WHEN CAST(SUBSTR(END_DATE_TIME,8,2) AS INTEGER) > 30 THEN LEFT(CONCAT(LEFT(END_DATE_TIME,7),'19',RIGHT(END_DATE_TIME,11)),11)\
            ELSE LEFT(CONCAT(LEFT(END_DATE_TIME,7),'20',RIGHT(END_DATE_TIME,11)),11)\
        END AS END_M_DATE_TIME,details.* \
        FROM details) d1 order by 1,2,3,4")

# COMMAND ----------

details_ltd.filter("EPISODE_ID IS NOT NULL AND DEATHS+INJURIES>0 AND (DAMAGED_PROPERTY NOT LIKE '0.00' OR DAMAGED_CROPS NOT LIKE '0.00') AND BEGIN_LAT IS NOT NULL AND LOCALITY NOT LIKE '%/%'").show(50,truncate=False)

# COMMAND ----------

spark.sql("SELECT STATE,COUNT(*) FROM details group by 1 order by 2 desc").show(50)

# COMMAND ----------

spark.sql("SELECT CAST(LEFT(BEGIN_YEARMONTH,4) AS INT) AS YEAR,COUNT(*) FROM details group by 1 order by 2 desc").show(50)

# COMMAND ----------

details_ltd.createOrReplaceTempView('details_ltd')

# COMMAND ----------

details_ltd=details_ltd.withColumn('year',year(details_ltd.BEGIN_TIMESTAMP))

# COMMAND ----------

details_parted20=spark.sql("SELECT 88850*FLOOR(ROWNUM/88850) AS PARTN,d1.* FROM (SELECT ROW_NUMBER() OVER (ORDER BY BEGIN_TIMESTAMP,END_TIMESTAMP,EPISODE_ID,EVENT_ID) AS ROWNUM,details_ltd.* FROM details_ltd) d1 ORDER BY ROWNUM")

# COMMAND ----------

details_parted=spark.sql("SELECT 218920*FLOOR(ROWNUM/218920) AS PARTN,d1.* FROM (SELECT ROW_NUMBER() OVER (ORDER BY BEGIN_TIMESTAMP,END_TIMESTAMP,EPISODE_ID,EVENT_ID) AS ROWNUM,details_ltd.* FROM details_ltd) d1 ORDER BY ROWNUM")

# COMMAND ----------

details_parted.createOrReplaceTempView('details_parted')

# COMMAND ----------

spark.sql('select PARTN,count(*) from details_parted group by 1 order by 1').show()

# COMMAND ----------

df_fatalities=df_fatalities.withColumn('FATALITY_DATE',when(df_fatalities.EVENT_ID == 402331, '07/04/2012 11:00:00')\
                         .when(df_fatalities.EVENT_ID == 402384, '07/18/2012 11:00:00').\
                         otherwise(df_fatalities.FATALITY_DATE))

# COMMAND ----------

df_fatalities.createOrReplaceTempView('fatalities')

# COMMAND ----------

df_fatalities.show()

# COMMAND ----------

fatalities_ltd=spark.sql("SELECT \
        CASE WHEN SUBSTR(FATALITY_DATE,2,1) = '/' AND LEFT(RIGHT(FATALITY_DATE,6),1) = ':' THEN TO_TIMESTAMP(FATALITY_DATE,'M/dd/yyyy HH:mm:ss') \
             WHEN SUBSTR(FATALITY_DATE,2,1) = '/' AND LEFT(RIGHT(FATALITY_DATE,6),1) = ' ' THEN TO_TIMESTAMP(FATALITY_DATE,'M/dd/yyyy HH:mm') \
             ELSE TO_TIMESTAMP(FATALITY_DATE,'MM/dd/yyyy HH:mm:ss') \
        END AS FATALITY_TIMESTAMP,\
        * FROM fatalities order by FATALITY_TIMESTAMP,EVENT_ID,FATALITY_ID")

# COMMAND ----------

fatalities_ltd=fatalities_ltd.withColumn('year',year(fatalities_ltd.FATALITY_TIMESTAMP))

# COMMAND ----------

fatalities_ltd.createOrReplaceTempView('fatalities_ltd')

# COMMAND ----------



# COMMAND ----------

fatalities_parted=spark.sql("select 2560*FLOOR(ROWNUM/2560) AS PARTN,f1.* FROM (SELECT ROW_NUMBER() OVER (ORDER BY FATALITY_TIMESTAMP,EVENT_ID,FATALITY_ID) AS ROWNUM,fatalities_ltd.* from fatalities_ltd) f1 ORDER BY ROWNUM")

# COMMAND ----------

fatalities_parted20=spark.sql("select 1020*FLOOR(ROWNUM/1020) AS PARTN,f1.* FROM (SELECT ROW_NUMBER() OVER (ORDER BY FATALITY_TIMESTAMP,EVENT_ID,FATALITY_ID) AS ROWNUM,fatalities_ltd.* from fatalities_ltd) f1 ORDER BY ROWNUM")

# COMMAND ----------

fatalities_parted.createOrReplaceTempView('fatalities_parted')

# COMMAND ----------

fatalities_parted.orderBy(['PARTN','ROWNUM'],ascending=[False,False]).show()

# COMMAND ----------

spark.sql('select PARTN,count(*) from fatalities_parted group by 1 order by 1').show()

# COMMAND ----------

#details_ltd.write.partitionBy("year").mode("overwrite").parquet("dbfs:/mnt/storm/details")
#fatalities_ltd.write.partitionBy("year").mode("overwrite").parquet("dbfs:/mnt/storm/fatalities")

# COMMAND ----------

details_parted.write.partitionBy("PARTN").mode("overwrite").parquet("dbfs:/mnt/storm/details")
fatalities_parted.write.partitionBy("PARTN").mode("overwrite").parquet("dbfs:/mnt/storm/fatalities")

# COMMAND ----------

details_parted20.write.partitionBy("PARTN").mode("overwrite").parquet("dbfs:/mnt/storm/details_part20")
fatalities_parted20.write.partitionBy("PARTN").mode("overwrite").parquet("dbfs:/mnt/storm/fatalities_part20")

# COMMAND ----------

details_ltd.write.mode("overwrite").parquet("dbfs:/mnt/storm/details_autopart")
fatalities_ltd.write.mode("overwrite").parquet("dbfs:/mnt/storm/fatalities_autopart")

# COMMAND ----------

details_dist=spark.read.format("parquet").load('/mnt/storm/details/')
print('count of details loaded to spark partitioned as parquet: '+str(details_dist.count()))

# COMMAND ----------

details_autopart=spark.read.format("parquet").load('/mnt/storm/details_autopart/')
print('count of details loaded to spark partitioned as default partitioned parquet: '+str(details_autopart.count()))

# COMMAND ----------

details_dist20=spark.read.format("parquet").load('/mnt/storm/details_part20/')
print('count of details loaded to spark partitionedx20 as parquet: '+str(details_dist.count()))

# COMMAND ----------

print('count of fatalities loaded to spark nonpartitioned: '+str(df_fatalities.count()))

# COMMAND ----------

fatalities_autopart=spark.read.format("parquet").load('/mnt/storm/fatalities_autopart/')
print('count of fatalities loaded to spark partitioned as parquet: '+str(fatalities_autopart.count()))

# COMMAND ----------

df_details = spark.read.format("csv").option("header", True).schema(schema_details).load("wasbs://allfiles@pipelinestorageacctaus.blob.core.windows.net/details/*.gz")
print('count of details loaded to spark nonpartitioned: ' +  str(df_details.count()))

# COMMAND ----------

details_autopart.groupBy(['year']).count().orderBy('year',ascending=False).show(10)

# COMMAND ----------

details_autopart.groupBy(['year','STATE','EVENT_TYPE']).count().orderBy(['year','STATE','EVENT_TYPE'],ascending=False).show(10)

# COMMAND ----------

print(f'count(DISTINCT(EVENT_TYPE)) = {details_autopart.select("EVENT_TYPE").distinct().count()}')

# COMMAND ----------

sc = SparkContext

def count_elements(splitIndex, iterator):
    n = sum(1 for _ in iterator)
    yield (splitIndex, n)

numparts = details_autopart.rdd.getNumPartitions()
sc.parallelize(numSlices=numparts,c)
details_def_rdd = sc.parallelize(range(0,numparts), numparts).map(lambda x: (x, x)).cache()
sizeparts = details_def_rdd.mapPartitionsWithIndex(lambda ind, x: count_elements(ind, x)).take(numparts)
#sizeparts = details_autopart.rdd.mapPartitionsWithIndex(lambda x,it: [(x,sum(1 for _ in it))]).collect()
#minsize=min(sizeparts,key=lambda item:item[1])
#maxsize=max(sizeparts,key=lambda item:item[1])
#print(f'default partitioning of details table created {numparts} partitions, with sizes of {sizeparts}')

# COMMAND ----------

details_dist.withColumn('year',year(details_dist.BEGIN_TIMESTAMP)).groupBy(['year']).count().orderBy('year',ascending=False).show(10)
#details_dist.groupBy(['year']).count().orderBy('year',ascending=False).show(10)

# COMMAND ----------

#df_details = spark.read.format("csv").option("header", True).schema(schema_details).load("wasbs://allfiles@pipelinestorageacctaus.blob.core.windows.net/details/*.gz")
df_details.groupBy(['YEAR']).count().orderBy('YEAR',ascending=False).show(10)

# COMMAND ----------

details_dist20=details_dist20.withColumn('year',year(details_dist20.BEGIN_TIMESTAMP))

# COMMAND ----------

details_dist20.groupBy(['year']).count().orderBy('year',ascending=False).show(10)

# COMMAND ----------

details_dist.createOrReplaceTempView('details_dist')

# COMMAND ----------

print(f'count(DISTINCT(EVENT_TYPE)) = {details_dist.select("EVENT_TYPE").distinct().count()}')

# COMMAND ----------

spark.sql('select count(distinct(EVENT_TYPE)) from details_dist').show()

# COMMAND ----------

spark.sql('select count(distinct(EVENT_TYPE)) from details').show()

# COMMAND ----------

print(f'count(DISTINCT(EVENT_TYPE)) = {details_dist20.select("EVENT_TYPE").distinct().count()}')

# COMMAND ----------

details_dist.withColumn('year',year(details_dist.BEGIN_TIMESTAMP)).groupBy(['year','STATE','EVENT_TYPE']).count().orderBy(['year','STATE','EVENT_TYPE'],ascending=False).show(10)
#details_dist.groupBy(['year']).count().orderBy('year',ascending=False).show(10)

# COMMAND ----------

df_details.groupBy(['year','STATE','EVENT_TYPE']).count().orderBy(['year','STATE','EVENT_TYPE'],ascending=False).show(10)

# COMMAND ----------

details_disty = details_dist.withColumn('year',year(details_dist.BEGIN_TIMESTAMP))

# COMMAND ----------

details_disty.groupBy(['year','STATE','EVENT_TYPE']).count().orderBy(['year','STATE','EVENT_TYPE'],ascending=False).show(10)

# COMMAND ----------

details_dist20.groupBy(['year','STATE','EVENT_TYPE']).count().orderBy(['year','STATE','EVENT_TYPE'],ascending=False).show(10)

# COMMAND ----------

df_details.count()

# COMMAND ----------

details_dist.count()

# COMMAND ----------

details_dist20.count()

# COMMAND ----------

details_autopart.count()

# COMMAND ----------



# COMMAND ----------

print('This cluster has 2 worker nodes with each node having 4 CPU cores = 8 total CPU cores.\n\nI chose explicit parquet partitions count of:\n\t8 (i.e. 1 partition per core)\n\t20 (per Spark documentation recommendation of 2.5 tasks per core)\n\nIn addition, I also tested the default partitioning given when not explictly defining the partioning scheme:\n\t9 partitions of details / 1 partition for fatalities.\n\nFinally, I benchmarked each against the non-partitioned, non-parquet dataframe given by importing the source csvs')

# COMMAND ----------

print('speedups = ratio of elapsed time using each of the following vs non-partitioned:\n\t 1)  8 parquet partitions\n\t 2)  9 parquet partitions (DEFAULT, i.e. no separate folders per partition)\n\t 3) 20 parquet partitions')

# COMMAND ----------

print('count full details:')
print(f'\tspeedup 1 = {pyround(3.43/.26,2)}x')
print(f'\tspeedup 2 = {pyround(3.43/.22,2)}x')
print(f'\tspeedup 3 =  {pyround(3.43/.43,2)}x')

# COMMAND ----------

print('counting distinct details event_types:')
print(f'\tspeedup 1 = {pyround(4.44/.44,2)}x')
print(f'\tspeedup 2 =  {pyround(4.44/.54,2)}x')
print(f'\tspeedup 3 =  {pyround(4.44/.69,2)}x')

# COMMAND ----------

print('counting details by year:')
print(f'\tspeedup 1 =  {pyround(4.24/.57,2)}x')
print(f'\tspeedup 2 = {pyround(4.24/.36,2)}x')
print(f'\tspeedup 3 =  {pyround(4.24/.73,2)}x')

# COMMAND ----------

print('counting details by year,state, and event_type:')
print(f'\tspeedup 1 - {pyround(4.65/.77,2)}x')
print(f'\tspeedup 2 = {pyround(4.65/.62,2)}0x')
print(f'\tspeedup 3 = {pyround(4.65/.85,2)}x')
