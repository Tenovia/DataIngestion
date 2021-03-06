import datetime
from pyspark.context import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
if __name__ == '__main__':
    spark = SparkSession \
        .builder \
        .appName("reading csv") \
        .getOrCreate()

today=datetime.date.today()
for x in range(1,8):
    date1=today-datetime.timedelta(days=x)
    date1=str(date1)
    arr=date1.split("-")
    year=arr[0]
    month=arr[1]
    try:
        data_file ="s3://paragon-datalake/FacebookAds/landing_device/"+"device_"+date1+".csv"

        df= spark.read.csv(data_file, header=True,inferSchema=True, sep=",").cache()

        df.write.mode('overwrite').parquet("s3://paragon-datalake/FacebookAds/processing_device/parquet/"+year+"/"+month+"/"+"device_"+date1)
    except:
        continue
