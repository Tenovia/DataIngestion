from boto.mws.connection import MWSConnection 
import csv 
import cred
import importtos3
import datetime
MarketPlaceID = cred.marketplaceid()
MerchantID = cred.merchantid()
AccessKeyID = cred.accessid()
SecretKey = cred.secretkey()

mws = MWSConnection(AccessKeyID,SecretKey)

mws.SellerId = MerchantID
mws.Merchant = MerchantID
mws.MarketplaceId = MarketPlaceID


def Flat_File_Open_Listings_Data(yesterday,tomorrow):
   d=mws.get_report_request_list(MaxCount=1,ReportTypeList=['_GET_FLAT_FILE_OPEN_LISTINGS_DATA_'],RequestedFromDate=yesterday,RequestedToDate=tomorrow)
   data=""
   for i in d.GetReportRequestListResult.ReportRequestInfo:
       #print "\n\n----------------",i.ReportType,i.GeneratedReportId,"-------------------------"


       if(i.ReportType!="FeedSummaryReport"):
           reportid=str(i.GeneratedReportId)
           report = mws.get_report(ReportId=reportid)
    
           #print report
           data+=report
   date = datetime.date.today()
   date=str(date)
   datelist=date.split('-')
   address='marketing/amazonSellerCentral/'+datelist[0]+'/'+datelist[1]+'/'
  
   importtos3.write_to_s3(data,'paragon-datalake',address+'Flat_File_Open_Listings_Data'+date+'.csv')
def Merchant_Listings_All_Data(yesterday,tomorrow):
   d=mws.get_report_request_list(MaxCount=1,ReportTypeList=['_GET_MERCHANT_LISTINGS_ALL_DATA_'],RequestedFromDate=yesterday,RequestedToDate=tomorrow)
   data=""
   for i in d.GetReportRequestListResult.ReportRequestInfo:
       #print "\n\n----------------",i.ReportType,i.GeneratedReportId,"-------------------------"


       if(i.ReportType!="FeedSummaryReport"):
           reportid=str(i.GeneratedReportId)
           report = mws.get_report(ReportId=reportid)
    
           #print report
           data+=report
   date = datetime.date.today()
   date=str(date)
   datelist=date.split('-')
   address='marketing/amazonSellerCentral/'+datelist[0]+'/'+datelist[1]+'/'
  
   importtos3.write_to_s3(data,'paragon-datalake',address+'Merchant_Listings_All_Data'+date+'.csv')
    
def main():
    today = datetime.date.today()
    yesterday = str(today - datetime.timedelta(days = 1))
    tomorrow = str(today + datetime.timedelta(days = 1))
    today=str(today)
    #d=mws.request_report(ReportType='_GET_FLAT_FILE_OPEN_LISTINGS_DATA_',StartDate=yesterday,EndDate=today)
    #d=mws.request_report(ReportType='_GET_MERCHANT_LISTINGS_ALL_DATA_',StartDate=yesterday,EndDate=today)
	
    Flat_File_Open_Listings_Data(yesterday,tomorrow)
    Merchant_Listings_All_Data(yesterday,tomorrow)
main()
def lambda_handler(context,switch):
    main()
    print "success"
    
