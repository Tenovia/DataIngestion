import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
from pyspark import SparkConf
from pyspark.sql.functions import col, unix_timestamp, to_date
import datetime
from collections import defaultdict

spark = SparkSession.builder.appName('App1').config(conf=SparkConf()).getOrCreate()

today = datetime.date.today()
for i in range(1,9):
    full_date = str(today - datetime.timedelta(days = i))
      
    #data = r"C:\Users\Mihir Chhatre\Desktop\Tenovia\Reports\age_report.csv"
    data = "s3://paragon-datalake/GoogleAds/landing/geo_report/geo_report_"+full_date+".csv"
    df = spark.read.format('csv').options(header='true', inferSchema='true').load(data)

    df1 = df.toDF('AdGroupName','AdGroupStatus','AllConversions','AverageCpc',
                     'AverageCpm','AverageCpv','CampaignName','CampaignStatus',
                     'CityCriteriaId','Clicks','ConversionRate','Conversions',
                     'Cost','Ctr','Date','CustomerDescriptiveName','DayOfWeek','Device','Impressions',
                     'InteractionRate','Interactions','LocationType',
                     'MetroCriteriaId','VideoViews','RegionCriteriaId',
                     'CountryID')
    d = {'20452': 'Andaman and Nicobar Islands', '20453': 'Andhra Pradesh', '20454': 'Assam',
     '20455': 'Bihar', '20456': 'Delhi', '20457': 'Gujarat', '20458': 'Haryana', 
     '20459': 'Jammu and Kashmir', '20460': 'Karnataka', '20461': 'Kerala', '20462': 'Maharashtra',
     '20463': 'Meghalaya', '20464': 'Madhya Pradesh', '20465': 'Odisha', '20466': 'Punjab', '20467': 'Puducherry',
     '20468': 'Rajasthan', '20469': 'Tamil Nadu', '20470': 'Tripura', '20471': 'Uttar Pradesh',
     '20472': 'West Bengal', '21268': 'Goa', '21289': 'Arunachal Pradesh', '21334': 'Chhattisgarh',
     '21335': 'Himachal Pradesh', '21336': 'Jharkhand', '21337': 'Manipur', '21338': 'Mizoram', 
     '21339': 'Nagaland', '21340': 'Sikkim', '21341': 'Uttarakhand', '21342': 'Chandigarh',
     '21343': 'Dadra and Nagar Haveli', '21344': 'Daman and Diu', '21345': 'Lakshadweep',
     '9061642': 'Telangana'}
    d=defaultdict(lambda:"not in india",d)

    lol= list(map(list,d.items()))
    mm = spark.createDataFrame(lol,["col1", "col2"])

    df3 = mm.toDF('RegionCriteriaId','Name')

    df4 = df1.join(df3,'RegionCriteriaId')


    df4 = df4.withColumn('cost',df4.Cost/1000000)
    df4 = df4.withColumn('AvgCpc',df4.AverageCpc/1000000)
    df4 = df4.withColumn('AvgCpm',df4.AverageCpm/1000000)
    df4 = df4.withColumn('AvgCpv',df4.AverageCpv/1000000)
    #df1.select(df1.NewCost,df1.AvgCpc,df1.AvgCpm,df1.AvgCpv).show()

    df4 = df4.drop("Cost","AverageCpm","AverageCpc","AverageCpv")


    df4.write.mode("overwrite").parquet("s3://paragon-datalake/GoogleAds/processing/geo_parquet/geo_report_"+full_date)
