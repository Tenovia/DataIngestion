#!/usr/bin/env python
#
# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
The Keywords Performance report includes all statistics aggregated at the keyword level, one row per keyword.
If other segment fields are used, you may get more than one row per keyword.

The LoadFromStorage method is pulling credentials and properties from a
"googleads.yaml" file. By default, it looks for this file in your home
directory. For more information, see the "Caching authentication information"
section of our README.

"""

import locale
import sys
import _locale
import datetime
import importtos3

_locale._getdefaultlocale = (lambda *args: ['en_US', 'UTF-8'])
#these above steps are necessary for UTF-8


from googleads import adwords

def main(client,date,full_date):
  # Initialize appropriate service.
  report_downloader = client.GetReportDownloader(version='v201809')

  # Create report query.
  report_query = (adwords.ReportQueryBuilder()
                  .Select('AccountDescriptiveName','AdGroupName','AdGroupStatus','AverageCpc','AverageCpe',
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
                  'VideoViews') # these are the fields we are using to generate our report
                  .From('KEYWORDS_PERFORMANCE_REPORT')  #name of the report
                  #.Where('Status').In('ENABLED')    #we can filter the attribiutes we are pulling using where clause
                  .During(date) # custom date can be specified ('DURING 20150201,20150301')
                  .Build())

  x=(report_downloader.DownloadReportAsStringWithAwql(
        report_query, 'CSV', skip_report_header=True, skip_column_header=False,
        skip_report_summary=True, include_zero_impressions=True))
  #print(x)      #we are printing the report and storing it in a CSV file
  f=open("keyword_report"+full_date+".csv","w")
  f.write(x)
  f.close()

  #l = full_date.split("-")
  filename = "GoogleAds/landing/keyword_report/"+"keyword_report_"+full_date+".csv"
  importtos3.write_to_s3(x,'paragon-datalake',filename)




if __name__ == '__main__':
    # Initialize client object.
    adwords_client = adwords.AdWordsClient.LoadFromStorage()
    today = datetime.date.today()
    for i in range(1,9):
        full_date = str(today - datetime.timedelta(days = i))
        year_month_date = full_date.split("-")
        date = ''.join(year_month_date)
        date = date+','+date        #this date is formatted in a way to pass to the during parameter
        #print(date,full_date)
        #print(type(full_date))
        main(adwords_client,date,full_date)


    
