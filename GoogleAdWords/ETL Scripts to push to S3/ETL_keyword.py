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
    data = "s3://paragon-datalake/GoogleAds/landing/keyword_report/keyword_report_"+full_date+".csv"
    df = spark.read.format('csv').options(header='true', inferSchema='true').load(data)

    df1 = df.toDF('AccountDescriptiveName','AdGroupName','AdGroupStatus','AverageCpc','AverageCpe',
                  'AverageCpm','AverageCpv','AveragePageviews','AveragePosition','AverageTimeOnSite','BounceRate',
                  'CampaignName','CampaignStatus','ClickAssistedConversions','ClickAssistedConversionsOverLastClickConversions',
                  'ClickAssistedConversionValue','Clicks','Conversions','Cost','CostPerConversion',
                  'CriteriaDestinationUrl','Ctr','CustomerDescriptiveName','Date','DayOfWeek','Engagements',
                  'EngagementRate','EstimatedAddClicksAtFirstPositionCpc','EstimatedAddCostAtFirstPositionCpc',
                  'HistoricalCreativeQualityScore','HistoricalQualityScore','HistoricalSearchPredictedCtr',
                  'ImpressionAssistedConversions','ImpressionAssistedConversionsOverLastClickConversions',
                  'ImpressionAssistedConversionValue','Impressions','InteractionRate','Interactions','KeywordMatchType','PercentNewVisitors',
                  'QualityScore','SearchAbsoluteTopImpressionShare','SearchBudgetLostAbsoluteTopImpressionShare','SearchBudgetLostTopImpressionShare',
                  'SearchImpressionShare','SearchPredictedCtr','SearchRankLostAbsoluteTopImpressionShare','SearchRankLostImpressionShare',
                  'SearchRankLostTopImpressionShare','Status','SystemServingStatus','TopImpressionPercentage','TopOfPageCpc',
                  'VideoQuartile100Rate','VideoQuartile50Rate','VideoQuartile75Rate','VideoQuartile25Rate','VideoViewRate',
                  'VideoViews')

    df1 = df1.withColumn('cost',df1.Cost/1000000)
    df1 = df1.withColumn('AvgCpm',df1['AverageCpm']/1000000)
    df1 = df1.withColumn('AvgCpc',df1['AverageCpc']/1000000)
    df1 = df1.withColumn('AvgCpv',df1['AverageCpv']/1000000)
    df1 = df1.withColumn('AvgCpe',df1['AverageCpe']/1000000)
    df1 = df1.withColumn('CostPerConv',df1['CostPerConversion']/1000000)

    df1 = df1.drop("AverageCpc","AverageCpm","AverageCpv","AverageCpe","Cost","CostPerConversion")

    df1.write.mode("overwrite").parquet("s3://paragon-datalake/GoogleAds/processing/keyword_parquet/keyword_report_"+full_date)

