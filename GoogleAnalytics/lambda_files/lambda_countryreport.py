"""Hello Analytics Reporting API V4."""
"""Please check this link https://ga-dev-tools.appspot.com/dimensions-metrics-explorer/ to get the information about filters and dimensions

Created by:Akhil Upadhyay

mail:akhil@tenovia.com

purpose:To access the Analytics data from google Reporting v4 api
"""


from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import datetime 
import view_id
'''Providing the url, file location of key accesses and View ID which can be accessed from user settings in admin accounts'''




import importtos3
SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = 'client_secrets.json'
VIEW_ID = view_id.get_view_id()


def initialize_analyticsreporting():
  """Initializes an Analytics Reporting API V4 service object.

  Returns:
    An authorized Analytics Reporting API V4 service object.
  """
  credentials = ServiceAccountCredentials.from_json_keyfile_name(
      KEY_FILE_LOCATION, SCOPES)

  # Build the service object.
  analytics = build('analyticsreporting', 'v4', credentials=credentials)

  return analytics


def get_report(analytics,date,startdate):

  """Queries the Analytics Reporting API V4.

  Args:
    analytics: An authorized Analytics Reporting API V4 service object.
  Returns:
    The Analytics Reporting API V4 response.
  """

  headers=""
  list_dimension=[{'name': 'ga:country'},{'name': 'ga:city'},{'name':'ga:date'}]
  list_metrics=[{'expression':'ga:users'},{'expression':'ga:newusers'},{'expression': 'ga:sessions'},{'expression':'ga:bounceRate'},{'expression':'ga:pageviewsPerSession'},{'expression':'ga:avgSessionDuration'},{'expression':'ga:transactions'},{'expression':'ga:transactionRevenue'},{'expression':'ga:transactionsPerSession'}]
  list_date=[{'startDate': startdate, 'endDate': date}]
  for items in list_dimension:
    #print items['name'][3:],
    headers+=(items['name'][3:]+"	")
  for items in list_metrics:
    #print items['expression'][3:],],
    headers+=items['expression'][3:]+"	"
  headers+="\n"
  return analytics.reports().batchGet(
      body={
        'reportRequests': [
        {
          'viewId': VIEW_ID,
          'dateRanges': list_date,
          'metrics': list_metrics,
          'dimensions': list_dimension
        }]
      }
  ).execute(),headers


def print_response(response,date,headers,startdate):
  """Parses and prints the Analytics Reporting API V4 response.

  Args:
    response: An Analytics Reporting API V4 response.
  """
  stringfordata=headers

  for report in response.get('reports', []):
    columnHeader = report.get('columnHeader', {})
    dimensionHeaders = columnHeader.get('dimensions', [])
    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])

    for row in report.get('data', {}).get('rows', []):
      dimensions = row.get('dimensions', [])
      dateRangeValues = row.get('metrics', [])

      for header, dimension in zip(dimensionHeaders, dimensions):
        stringfordata+=( dimension+'	')                      			 #dimension based on which report is accessed 
      
      for i, values in enumerate(dateRangeValues):
        for metricHeader, value in zip(metricHeaders, values.get('values')):
          stringfordata+=( value+'	')						#to get the data into csv format
        stringfordata+="\n"
  #print(stringfordata)
  

  address="googleanalytics/landing/countryreport/"
  file_name=address+"countryreport"+date+".csv"
  importtos3.write_to_s3(stringfordata,'paragon-datalake',file_name)
  
  '''
  text_file = open("countryreport.csv", "w")
  n = text_file.write(stringfordata)
  text_file.close()
  '''
  
  #print(stringfordata)
  

	
def main():
	analytics = initialize_analyticsreporting()


	
	date1 = datetime.date.today()
	for i in range(1,9):
		startdate=str(date1-datetime.timedelta(days=i))
		date=str(date1-datetime.timedelta(days=i))
	
		response,headers = get_report(analytics,date,startdate)
		print_response(response,date,headers,startdate)


if __name__ == '__main__':
  main()


def lambda_handler(context,switch):
  main()
