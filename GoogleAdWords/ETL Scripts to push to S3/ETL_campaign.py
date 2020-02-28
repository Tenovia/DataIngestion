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
    data = "s3://paragon-datalake/GoogleAds/landing/campaign_report/campaign_report_"+full_date+".csv"
    df = spark.read.format('csv').options(header='true', inferSchema='true').load(data)

    df1 = df.toDF('AccountDescriptiveName','Amount','AverageCost','AverageCpc','AverageCpe','AverageCpm','AverageCpv',
                      'AveragePosition','BounceRate','CampaignName','AverageTimeOnSite','AverageFrequency',
                      'AveragePageviews',
                      'CampaignStatus','CampaignTrialType','ClickAssistedConversions','ClickAssistedConversionsOverLastClickConversions',
                      'ClickAssistedConversionValue','Clicks','ContentBudgetLostImpressionShare','ContentImpressionShare',
                      'ContentRankLostImpressionShare','Conversions','Cost','CostPerConversion','Ctr','CustomerDescriptiveName',
                      'Date','EndDate','StartDate','GmailForwards','GmailSaves','GmailSecondaryClicks','HasRecommendedBudget',
                      'ImpressionAssistedConversions','ImpressionAssistedConversionsOverLastClickConversions','ImpressionAssistedConversionValue',
                      'ImpressionReach','Impressions','Interactions','InteractionRate','InvalidClickRate','InvalidClicks','IsBudgetExplicitlyShared',
                      'PercentNewVisitors','Period','RecommendedBudgetAmount','RelativeCtr','SearchAbsoluteTopImpressionShare',
                      'SearchBudgetLostAbsoluteTopImpressionShare','SearchBudgetLostImpressionShare','SearchBudgetLostTopImpressionShare',
                      'SearchClickShare','SearchExactMatchImpressionShare','SearchImpressionShare','SearchRankLostAbsoluteTopImpressionShare',
                      'SearchRankLostImpressionShare','SearchRankLostTopImpressionShare','SearchTopImpressionShare','ServingStatus',
                      'VideoQuartile75Rate','VideoQuartile25Rate','VideoQuartile50Rate','VideoQuartile100Rate','VideoViews',
                      'VideoViewRate')
    df1 = df1.withColumn('cost',df1.Cost/1000000)
    df1 = df1.withColumn('amount',df1.Amount/1000000)
    df1 = df1.withColumn('AvgCpm',df1['AverageCpm']/1000000)
    df1 = df1.withColumn('AvgCpc',df1['AverageCpc']/1000000)
    df1 = df1.withColumn('AvgCpv',df1['AverageCpv']/1000000)
    df1 = df1.withColumn('AvgCpe',df1['AverageCpe']/1000000)
    df1 = df1.withColumn('CostPerConv',df1['CostPerConversion']/1000000)
    df1 = df1.withColumn('RecommendedBudgetAmt',df1['RecommendedBudgetAmount']/1000000)

    df1 = df1.drop("Cost","Amount","AverageCpm","AverageCpc","AverageCpv","AverageCpe","RecommendedBudgetAmount")

    df1.write.mode("overwrite").parquet("s3://paragon-datalake/GoogleAds/processing/campaign_parquet/campaign_report_"+full_date)

