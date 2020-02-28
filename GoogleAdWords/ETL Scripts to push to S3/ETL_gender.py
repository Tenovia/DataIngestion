import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
from pyspark import SparkConf
from pyspark.sql.functions import col, unix_timestamp, to_date
import datetime

spark = SparkSession.builder.appName('App1').config(conf=SparkConf()).getOrCreate()

today = datetime.date.today()
for i in range(1,9):
    full_date = str(today - datetime.timedelta(days = i))
      
    #data = r"C:\Users\Mihir Chhatre\Desktop\Tenovia\Reports\age_report.csv"
    data = "s3://paragon-datalake/GoogleAds/landing/gender_report/gender_report_"+full_date+".csv"
    df = spark.read.format('csv').options(header='true', inferSchema='true').load(data)

    df1 = df.toDF('CampaignName','CampaignStatus','AdGroupName','AdGroupStatus','AverageCpc','AverageCpe',
                     'AverageCpm','AverageCpv','Clicks','Conversions','ConversionRate',
                     'Cost','Ctr','Date','CustomerDescriptiveName','DayOfWeek',
                     'Device','Impressions','Interactions','VideoViews','VideoQuartile25Rate',
                     'VideoQuartile50Rate','VideoQuartile75Rate','VideoQuartile100Rate',
                     'GmailForwards','GmailSaves','Status','Criteria')
    
    df1 = df1.withColumn('cost',df1.Cost/1000000)
    df1 = df1.withColumn('AvgCpc',df1.AverageCpc/1000000)
    df1 = df1.withColumn('AvgCpm',df1.AverageCpm/1000000)
    df1 = df1.withColumn('AvgCpv',df1.AverageCpv/1000000)
    df1 = df1.withColumn('AvgCpe',df1.AverageCpe/1000000)
    df1 = df1.withColumn('Gender',df1.Criteria)

    df1 = df1.drop("Cost","AverageCpm","AverageCpc","AverageCpv","AverageCpe","Criteria")

    df1.write.mode("overwrite").parquet("s3://paragon-datalake/GoogleAds/processing/gender_parquet/gender_report_"+full_date)
