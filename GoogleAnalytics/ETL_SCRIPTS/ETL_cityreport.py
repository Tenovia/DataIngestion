"""
Created by:Akhil Upadhyay
mail:akhil@tenovia.com
"""
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
from pyspark import SparkConf
import datetime
from pyspark.sql.functions import col, unix_timestamp, to_date
spark = SparkSession.builder.appName('App1').config(conf=SparkConf()).getOrCreate()
today=datetime.date.today()
for x in range(1,9):
    date1=str(today-datetime.timedelta(days=x))

    data = 's3://paragon-datalake/googleanalytics/landing/cityreport/cityreport'+date1+'.csv'

    df = spark.read.format('csv').options(header='true', inferSchema='true',sep='\t').load(data)
    
    l1=df.schema.fieldNames()
    l2=[]
    for header in l1:
        x="-".join(header.split(" "))
        l2.append(x)


    data=df.toDF(*l2)
    #data.show()
    data = data.withColumn("date",data["date"].cast('String'))
    data.printSchema()
    
    data= data.withColumn('date',to_date(unix_timestamp(col('date'), 'yyyyMMdd').cast("timestamp")))
    
    data.write.mode("overwrite").parquet('s3://paragon-datalake/googleanalytics/processing/cityreport/cityreport'+date1)
    
