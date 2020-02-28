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
The Age Range Performance report includes all Display Network and YouTube Network statistics
aggregated by age range. It also includes automatic audience performance.

The LoadFromStorage method is pulling credentials and properties from a
"googleads.yaml" file. By default, it looks for this file in your home
directory. For more information, see the "Caching authentication information"
section of our README.

"""

import locale
import sys
import _locale
import importtos3
import datetime

_locale._getdefaultlocale = (lambda *args: ['en_US', 'UTF-8'])
#these above steps are necessary for UTF-8

from googleads import adwords

def main(client,date,full_date):
    # Initialize appropriate service.
    report_downloader = client.GetReportDownloader(version='v201809')
    # Create report query.
    report_query = (adwords.ReportQueryBuilder()
                    .Select('CampaignName','CampaignId','CampaignStatus','AdGroupName','AdGroupStatus','AverageCpc','AverageCpe',
                        'AverageCpm','AverageCpv','Clicks','Conversions','ConversionRate',
                     'Cost','Ctr','CustomerDescriptiveName','Date','DayOfWeek',
                     'Device','VideoViews','VideoQuartile25Rate',
                     'VideoQuartile50Rate','VideoQuartile75Rate',
                    'VideoQuartile100Rate','Criteria','Status') #these are the fields that we are generating in our report
                    .From('AGE_RANGE_PERFORMANCE_REPORT')
                  #.Where('Status').In('ENABLED') #we can specify some criteria to filter the attributes selected above
                    .During(date)  #.(DURING '20150201,20150301') is another to specify the date
                    .Build())


    x=(report_downloader.DownloadReportAsStringWithAwql(
        report_query, 'CSV', skip_report_header=True, skip_column_header=False,
        skip_report_summary=True, include_zero_impressions=True))

    #print(x)         #we are priting the output and storing it in a CSV file

    f=open("age_report_"+full_date+".csv","w")
    f.write(x)
    f.close()


    #l = full_date.split("-")
    filename = "GoogleAds/landing/age_report/"+"age_report_"+full_date+".csv"
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

    '''eight_days_back = str(today - datetime.timedelta(days = 8))
    now = str(today - datetime.timedelta(days = 0))
    #today = datetime.date.today()
    #print(eight_days_back)
    #print(type(now))

    yyyymmdd1 = eight_days_back.split("-")
    eight_days_back = ''.join(yyyymmdd1)
    #print(eight_days_back)

    yyyymmdd2 = now.split("-")
    now = ''.join(yyyymmdd2)
    #print(now)

    date = eight_days_back+','+now
    #print(date)'''








