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
The Landing Page report includes all statistics aggregated by default by the UnexpandedFinalUrlString,
 one row per the URL string.

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
# these above lines are needed for UTF-8

from googleads import adwords

def main(client,date,full_date):
  # Initialize appropriate service.
  report_downloader = client.GetReportDownloader(version='v201809')

  # Create report query.
  report_query = (adwords.ReportQueryBuilder()
                  .Select('CampaignName','CampaignStatus','AdGroupName','AdGroupStatus','AverageCpc','AverageCpe',
                     'AverageCpm','AverageCpv','Clicks','Conversions','ConversionRate',
                     'Cost','Ctr','Date','DayOfWeek','Device','UnexpandedFinalUrlString','ExpandedFinalUrlString',
                     'Device','Impressions','Interactions','EngagementRate','PercentageMobileFriendlyClicks',
                     'PercentageValidAcceleratedMobilePagesClicks','SpeedScore','VideoViews')
                     # we are pulling the above fileds to generate our report
                  .From('LANDING_PAGE_REPORT')
                  #.Where('Status').In('ENABLED')   #to further filter our attributes being pulled using where clause
                  .During(date) #custom date can be specified (check age performance report for syntax)
                  .Build())

  x=(report_downloader.DownloadReportAsStringWithAwql(
        report_query, 'CSV', skip_report_header=True, skip_column_header=False,
        skip_report_summary=True))
  #print(x)      #we are printing the report and storing it in a CSV file
  f=open("landing_pg_report"+full_date+".csv","w")
  f.write(x)
  f.close()


  #l = full_date.split("-")
  filename = "GoogleAds/landing/landing_page_report/"+"landing_page_report_"+full_date+".csv"
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
